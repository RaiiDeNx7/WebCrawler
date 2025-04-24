#! python3.12
#!/usr/bin/env python
import sys
import requests

CONTROLLER = 'http://127.0.0.1:8000'

def do_status():
    r = requests.get(f'{CONTROLLER}/status')
    r.raise_for_status()
    print("=== Status ===")
    print(r.json())

def do_add(url):
    r = requests.post(f'{CONTROLLER}/add_url', json={'url': url})
    r.raise_for_status()
    print("=== Add URL ===")
    print(r.json())

def do_visited():
    r = requests.get(f'{CONTROLLER}/visited')
    r.raise_for_status()
    print("=== Visited URLs ===")
    for u in r.json():
        print(u)

def do_shutdown():
    r = requests.post(f'{CONTROLLER}/shutdown')
    # Note: shutdown endpoint may return plain text, not JSON
    print("=== Shutdown Controller ===")
    print(r.text)

def print_help():
    print("Usage: client.py <command> [args]\n")
    print("Commands:")
    print("  status            Show queue size, visited count, and queued URLs")
    print("  add <url>         Add a new URL to the crawl queue")
    print("  visited           List all visited URLs")

def main():
    if len(sys.argv) < 2:
        print("Error: no command provided.\n")
        print_help()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    try:
        if cmd == 'status':
            do_status()
        elif cmd == 'add':
            if len(sys.argv) < 3:
                print("Error: 'add' requires a URL argument.\n")
                print_help()
                sys.exit(1)
            do_add(sys.argv[2])
        elif cmd == 'visited':
            do_visited()
        elif cmd == 'shutdown':
            do_shutdown()
        else:
            print(f"Error: unknown command '{cmd}'.\n")
            print_help()
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


