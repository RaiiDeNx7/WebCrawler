import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class WebCrawler:
    def __init__(self):
        self.queue = deque()
        self.discovered_websites = set()
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def discover(self, root):
        self.queue.append(root)
        self.discovered_websites.add(root)

        while self.queue:
            v = self.queue.popleft()
            raw = self.read_url(v)

            regex = r'href=["\'](https?://[^"\']+)'  # Improved regex to extract full URLs
            matches = re.findall(regex, raw)
            
            for actual in matches:
                actual = urljoin(root, actual)  # Ensure proper absolute URLs
                if self.is_valid_url(actual) and actual not in self.discovered_websites:
                    self.discovered_websites.add(actual)
                    print(f"Website found: {actual}")
                    self.queue.append(actual)

    def read_url(self, v):
        raw = ""
        try:
            self.driver.get(v)
            time.sleep(2)  # Allow JavaScript to load if needed
            raw = self.driver.page_source
        except Exception as ex:
            print(f"Error fetching {v}: {ex}")
        return raw

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    crawler = WebCrawler()
    root_url = "https://www.google.com"
    crawler.discover(root_url)
    crawler.close()

