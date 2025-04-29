### worker/worker.py

import socket
import time
import requests
from bs4 import BeautifulSoup
from common.protocol import encode_message, decode_message, MSG_READY, MSG_URL, MSG_RESULT, MSG_NO_MORE_WORK
import os
import json
from urllib.parse import urlparse

CONTROLLER_HOST = os.getenv("CONTROLLER_HOST", "172.20.208.161:8000")
CONTROLLER_PORT = 5000

pid = os.getpid()

white_listed_sites = [
    "https://allrecipes.com",
    "https://foodnetwork.com",
    "https://epicurious.com",
    "https://bonappetit.com",
    "https://seriousseats.com",
    "https://tasty.co",
    "https://delish.com",
    "https://eatingwell.com",
    "https://thekitchn.com",
]

def has_recipe_schema(soup):
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            data = json.loads(script.string)
            # Sometimes the schema is a list
            if isinstance(data, list):
                for item in data:
                    if item.get('@type') == 'Recipe':
                        return True
            elif isinstance(data, dict):
                if data.get('@type') == 'Recipe':
                    return True
        except (json.JSONDecodeError, TypeError) as e:
            continue
    return False 



def crawl(url):
    time.sleep(1) # web crawlings looks more natural with waits
    links = []
    if not any(site in url for site in white_listed_sites):
        print(f"[Worker] {pid} Skipping {url} (not whitelisted)")
        return links

    print(f"[Worker] {pid} Crawling {url}")

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # if not has_recipe_schema(soup):
        #     print(f"[Worker] {pid} No Recipe schema found in {url}")
        #     return links

        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if "recipe" not in link:
                continue
            if not link.startswith('http'): # added thing to the url
                link = link if link[0] != '/' else link[1::]
                links.append(f"{url}/{link}")
            else:
                links.append(link)
    except Exception as e:
        print(f"[Worker] Error crawling {url}: {e}")
    return links


def worker_main():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((CONTROLLER_HOST, CONTROLLER_PORT))

                while True:
                    sock.sendall(encode_message(MSG_READY))
                    raw_msg = sock.recv(4096)
                    if not raw_msg:
                        break

                    msg_type, data = decode_message(raw_msg)

                    if msg_type == MSG_URL:
                        url = data.get("url") if isinstance(data, dict) else data
                        links = crawl(url)
                        result = {"links": links}
                        sock.sendall(encode_message(MSG_RESULT, result))

                    elif msg_type == MSG_NO_MORE_WORK:
                        print(f"[Worker] {pid} No more work. Shutting down.")
                        return
                    time.sleep(2)

        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(f"[Worker] {pid} Connection error: {e}. Retrying...")
            time.sleep(2)

if __name__ == "__main__":
    worker_main()
