from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin, urlparse

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Set up ChromeDriver path
service = Service("chromedriver")  # Ensure chromedriver is in your PATH

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Crawling function
def crawl_website(start_url, max_links=5):
    visited = set()
    to_visit = [start_url]

    while to_visit and len(visited) < max_links:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            driver.get(url)
            time.sleep(2)  # Allow page to load

            # Extract and print page title
            title = driver.title
            print(f"Visited: {url} | Title: {title}")

            visited.add(url)

            # Extract all links
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and href.startswith("http"):
                    # Ensure it's within the same domain
                    if urlparse(href).netloc == urlparse(start_url).netloc:
                        to_visit.append(href)

        except Exception as e:
            print(f"Error visiting {url}: {e}")

    print("Crawling finished.")
    driver.quit()

# Start crawling from an example website
crawl_website("https://foodispower.org/access-health/food-deserts/")

