# README.md

# Group Members
Isaac Watts
Hunter Smith
Taniyah Epps
Kiara Wilson

# Distributed WebCrawler

This project is a distributed web crawler composed of a **Controller** and multiple **Workers**.

## Structure

```bash
common/        # Protocol helpers for communication
controller/    # Controller server that manages the URL queue
worker/        # Worker clients that perform crawling
```

## Requirements
Docker instructions: 
1) Build the docker image:
```
sudo docker build -t webcrawler .
```

2) Run the controller first: **NOTE** On windows it will be cmd
```
sudo docker run -it --entrypoint bash webcrawler
```
```
python -m controller.controller
```

3) Run a worker on a the machine you ran the controller. 
```
sudo docker run -it --entrypoint bash webcrawler
```
```
python -m worker.worker
```
or
When you have to run using other machines, you need to find the controllers private ip address and use that. 
```
sudo docker run -e CONTROLLER_HOST="<CONTROLLER_PRIV_IP>" -it --entrypoint bash webcrawler
```
```
python -m worker.worker
```


Install the necessary Python libraries (Python 3.12):

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

## Running Client

```bash
py client.py status
py client.py add https://example.com
py client.py visited
py client.py shutdown
```

## Running on website

```bash
http://127.0.0.1:8000/status
http://127.0.0.1:8000/visited
http://127.0.0.1:8000/add_url?target=https://example.com
```

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




