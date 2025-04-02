import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from vinted_api import VintedApi




# Set up Selenium WebDriver and API
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
api = VintedApi()

def enforce_newest_first(url):
    """Ensure URL has order=newest_first parameter"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['order'] = ['newest_first']
    return urlunparse(parsed._replace(query=urlencode(params, doseq=True)))

def get_top_items():
    """Get URLs of top 8 items on page"""
    items = driver.find_elements(By.CSS_SELECTOR, 'a.new-item-box__overlay--clickable')
    return [item.get_attribute('href') for item in items[:8]]

def extract_item_id(url):
    """Extract numeric ID from item URL"""
    return urlparse(url).path.split('/')[2].split('-')[0]

def format_product_info(product):
    """Format product information for display"""
    if not product or not isinstance(product, dict):
        return "Could not retrieve product details"
    
    return f"""
📌 Title: {product.get('title', 'N/A')}
💰 Price: {product.get('price', {}).get('amount', 'N/A')} {product.get('price', {}).get('currency_code', '')}
🏷️ Brand: {product.get('brand_title', 'N/A')}
📏 Size: {product.get('size_title', 'N/A')}
🔄 Status: {product.get('status', 'N/A')}
🔗 URL: https://www.vinted.fr{product.get('path', '')}
🖼️ Main Image: {product.get('photo', {}).get('url', 'No image available')}
"""

# Initial setup
base_url = 'https://www.vinted.co.uk/catalog?time=1743516768&disabled_personalization=true&page=1&order=newest_first&currency=GBP&search_text=apple&brand_ids[]=54661'
monitor_url = enforce_newest_first(base_url)
seen_items = set()

try:
    print("Starting monitor - checking for new items every minute")
    while True:
        # Load page and get items
        driver.get(monitor_url)
        time.sleep(10)
        
        current_items = get_top_items()
        current_ids = {extract_item_id(url) for url in current_items}
        
        new_ids = current_ids - seen_items
        if new_ids:
            print(f"\nNew items at {time.strftime('%H:%M:%S')}:")
            for item_id in new_ids:
                # Get product details using the API
                product = api.getProduct(item_id)
                print(format_product_info(product))
                print("─" * 60)
            seen_items.update(new_ids)
        else:
            print(f"\nNo new items at {time.strftime('%H:%M:%S')}")
        
        time.sleep(49)  # Total cycle time ~1 minute

except KeyboardInterrupt:
    print("\nMonitoring stopped by user")
finally:
    driver.quit()