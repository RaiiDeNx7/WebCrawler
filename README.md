# README.md

# Distributed WebCrawler

This project is a distributed web crawler composed of a **Controller** and multiple **Workers**.

## Structure

```bash
common/        # Protocol helpers for communication
controller/    # Controller server that manages the URL queue
worker/        # Worker clients that perform crawling
```

## Requirements

Install the necessary Python libraries:

```bash
pip install requests beautifulsoup4
```

## Running the Controller

Start the controller server:

```bash
py -m  controller.controller

http:127.0.0.1:8000/status 
```

## Running Workers

Start one or more workers (in different terminals or machines):

```bash
python worker.py
```

You can run multiple workers to speed up crawling.

## How It Works

- Controller maintains a queue of URLs.
- Workers request URLs, crawl the pages, and send back discovered links.
- Controller adds new links to the queue (if not visited).
- Process continues until no URLs are left.

## Notes

- The Controller is multi-threaded and can handle multiple Workers.
- The communication is simple JSON over TCP sockets.

Enjoy crawling the web distributedly! 🚀





Flask for users:

See the status (how many URLs crawled, queue size, connected workers)

Submit new seed URLs manually

View crawled links maybe?

Start/stop crawling


Worker returned """ from (IP, Port)

Database to store 

