import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Set up Selenium WebDriver
options = Options()
options.headless = True  # Run in headless mode (no browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to ensure the URL has the `order=newest_first` parameter
def ensure_newest_first_order(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    # Force set order to newest_first (we know order parameter always exists)
    query_params['order'] = ['newest_first']
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url

# Function to fetch item links from the page
def fetch_item_links(url):
    print(f"Navigating to URL: {url}")
    driver.get(url)
    time.sleep(10)  # Wait for the page to load fully
    items = driver.find_elements(By.CSS_SELECTOR, 'a.new-item-box__overlay--clickable')

    item_links = [item.get_attribute('href') for item in items[:8]]  # Get the first 8 item links
    return item_links

# Function to extract item IDs from URLs
def extract_item_ids(urls):
    item_ids = []
    for url in urls:
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.split('/')
        item_id = path_segments[2]  # Extract the item ID from the URL path
        item_ids.append(item_id)
    return item_ids

# Base URL of the filtered search page (this can change)
base_url = 'https://www.vinted.co.uk/catalog?search_text=montbell%20jacket&time=1743464869&disabled_personalization=true&size_ids[]=207&size_ids[]=208&page=1&brand_ids[]=615130&color_ids[]=1&order=price_high_to_low&price_to=75&currency=GBP'

# Ensure the URL has the `order=newest_first` parameter
url = ensure_newest_first_order(base_url)

# Initialize the previous item IDs list
previous_item_ids = []

# Run the search every 30 seconds
try:
    first_run = True
    while True:
        print("Fetching items...")
        
        # Fetch the item links
        item_links = fetch_item_links(url)
        
        # Extract item IDs from the links
        current_item_ids = extract_item_ids(item_links)
        
        if first_run:
            first_run = False
            previous_item_ids = current_item_ids
            print("\nTracked item IDs:")
            for i, item_id in enumerate(previous_item_ids, start=1):
                print(f"{i}. {item_id}")
        else:
            # Find new item IDs by comparing with the previous list
            new_item_ids = [item_id for item_id in current_item_ids if item_id not in previous_item_ids]
            
            # Display new item IDs if found
            if new_item_ids:
                print("\nNew item IDs found:")
                for i, item_id in enumerate(new_item_ids, start=1):
                    print(f"{i}. {item_id}")
                previous_item_ids.extend(new_item_ids)
                print("---------------------------------------------------")
            else:
                print("\nNo new item IDs found.\n---------------------------------------------------")
        
        # Wait for 30 seconds before the next search
        time.sleep(30)
except KeyboardInterrupt:
    print("\nStopping the program...")
finally:
    driver.quit()