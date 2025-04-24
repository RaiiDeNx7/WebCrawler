import socket
import threading
import queue
import time
from flask import Flask, request, jsonify, send_from_directory
from common.protocol import encode_message, decode_message, MSG_READY, MSG_URL, MSG_RESULT, MSG_NO_MORE_WORK
import os

HOST = '0.0.0.0'
PORT = 5000

url_queue = queue.Queue()  # The thread-safe queue to store URLs
visited_urls = set()  # URLs that have already been crawled
queued_urls = set()  # URLs that are already in the queue
queue_lock = threading.Lock()

seed_urls = [
    'https://google.com',
    'https://example.org'
]

# Initialize the queue with seed URLs
with queue_lock:
    for url in seed_urls:
        url_queue.put(url)
        queued_urls.add(url)

app = Flask(__name__)


@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/recipe')
def serve_recipe():
    return send_from_directory('static', 'recipe.html')

@app.route('/about')
def serve_about():
    return send_from_directory('static', 'about.html')


@app.route('/status', methods=['GET'])
def status():
    with queue_lock:
        return jsonify({
            'queue_size': url_queue.qsize(),
            'visited_count': len(visited_urls),
            'queue_contents': list(queued_urls - visited_urls)
        })

@app.route('/add_url', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        new_url = request.json.get('url')
    else:  # GET method
        new_url = request.args.get('target')

    if new_url:
        with queue_lock:
            if new_url not in visited_urls and new_url not in queued_urls:
                url_queue.put(new_url)
                queued_urls.add(new_url)
        return jsonify({'status': 'URL added', 'url': new_url}), 200

    return jsonify({'error': 'No URL provided'}), 400


@app.route('/visited', methods=['GET'])
def get_visited():
    with queue_lock:
        return jsonify(list(visited_urls))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func:
        shutdown_func()
        return 'Server shutting down...'
    else:
        return 'Shutdown function not available.', 500

def handle_worker(conn, addr):
    print(f"[+] Worker connected from {addr} - Task Started")
    try:
        while True:
            raw_msg = conn.recv(4096)
            if not raw_msg:
                break

            msg_type, data = decode_message(raw_msg)

            if msg_type == MSG_READY:
                timeout = 5  # wait up to 5 seconds for new work
                waited = 0
                while waited < timeout:
                    with queue_lock:
                        if not url_queue.empty():
                            next_url = url_queue.get()
                            visited_urls.add(next_url)
                            queued_urls.discard(next_url)
                            conn.sendall(encode_message(MSG_URL, {"url": next_url, "assigned_to": str(addr)}))
                            print(f"[✓] Task for {next_url} handled by {addr}")
                            break
                    time.sleep(1)
                    waited += 1
                else:
                    conn.sendall(encode_message(MSG_NO_MORE_WORK))
                    print(f"[!] No more work for {addr}. Worker will shut down.")
                    break

            elif msg_type == MSG_RESULT:
                links = data.get("links", [])
                with queue_lock:
                    for link in links:
                        if link not in visited_urls and link not in queued_urls:
                            url_queue.put(link)
                            queued_urls.add(link)
    except Exception as e:
        print(f"[!] Error with worker {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Worker {addr} disconnected")

def start_worker_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[*] Controller listening for workers on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            worker_thread = threading.Thread(target=handle_worker, args=(conn, addr), daemon=True)
            worker_thread.start()
    except Exception as e:
        print(f"[!] Worker server error: {e}")
    finally:
        server_socket.close()

def main():
    threading.Thread(target=start_worker_server, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()