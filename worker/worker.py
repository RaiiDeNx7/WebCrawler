# worker/worker.py

import socket
import time
import requests
from bs4 import BeautifulSoup
from common.protocol import encode_message, decode_message, MSG_READY, MSG_URL, MSG_RESULT, MSG_NO_MORE_WORK

CONTROLLER_HOST = '127.0.0.1'
CONTROLLER_PORT = 5000

def crawl(url):
    print(f"[Worker] Crawling {url}")
    links = []
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if link.startswith('http'):
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
                        url = data
                        links = crawl(url)
                        result = {"links": links}
                        sock.sendall(encode_message(MSG_RESULT, result))

                    elif msg_type == MSG_NO_MORE_WORK:
                        print("[Worker] No more work. Shutting down.")
                        return

        except (ConnectionRefusedError, ConnectionResetError) as e:
            print(f"[Worker] Connection error: {e}. Retrying...")
            time.sleep(2)  # Retry after a short delay


if __name__ == "__main__":
    worker_main()