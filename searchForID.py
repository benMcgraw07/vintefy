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

# Base URL of the filtered search page (this can change)
base_url = 'https://www.vinted.co.uk/catalog?search_text=montbell%20jacket&time=1743450010&disabled_personalization=true&size_ids[]=207&size_ids[]=208&page=1&brand_ids[]=615130&color_ids[]=1&order=relevance&price_to=75&currency=GBP'

# Ensure the URL has the `order=newest_first` parameter
url = ensure_newest_first_order(base_url)

# Fetch the item links
item_links = fetch_item_links(url)

# Print the fetched item links
print("\nTop 8 item links:")
for i, link in enumerate(item_links, start=1):
    print(f"{i}. {link}")

# Close the driver
driver.quit()