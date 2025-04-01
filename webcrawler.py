import re
import time
import threading
from collections import deque
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

class WebCrawler:
    def __init__(self, max_threads=5):
        self.queue = deque()
        self.discovered_websites = set()
        self.lock = threading.Lock()  # To ensure thread safety when modifying shared data
        self.max_threads = max_threads
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def discover(self, root):
        self.queue.append(root)
        self.discovered_websites.add(root)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            while self.queue:
                url = self.queue.popleft()
                executor.submit(self.process_url, url)
    
    def process_url(self, url):
        raw = self.read_url(url)
        
        regex = r'href=["\'](https?://[^"\']+)'  # Extract full URLs
        matches = re.findall(regex, raw)
        
        for actual in matches:
            actual = urljoin(url, actual)  # Ensure proper absolute URLs
            if self.is_valid_url(actual):
                with self.lock:
                    if actual not in self.discovered_websites:
                        self.discovered_websites.add(actual)
                        print(f"Website found: {actual}")
                        self.queue.append(actual)
    
    def read_url(self, url):
        raw = ""
        try:
            self.driver.get(url)
            time.sleep(2)  # Allow JavaScript to load if needed
            raw = self.driver.page_source
        except Exception as ex:
            print(f"Error fetching {url}: {ex}")
        return raw
    
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    crawler = WebCrawler(max_threads=5)
    root_url = "https://foodispower.org/access-health/food-deserts/"
    crawler.discover(root_url)
    crawler.close()
