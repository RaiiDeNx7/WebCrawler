# WebCrawler
Web Crawler Project

Team Members: 
- Isaac Watts
- Kiara Wilson
- Hunter Smith
- Taniyah Epps

## Project Overview
The Distributed Web Crawler is designed to efficiently fetch and process web pages using parallel computing techniques. This project demonstrates the use of **Multiprocessing, Multithreading, and Interprocess Communication (IPC)** to improve runtime efficiency. The gathered data will be analyzed and summarized for meaningful insights.

## Project Description
The web crawler will:
- Identify stores that offer **healthy food options** and accept **SNAP, EBT, and other government assistance**.
- Provide **budget-friendly recipes** based on an individual’s **location** and available ingredients.
- Enhance **nutrition accessibility** and improve food benefit utilization in underserved communities.

## Goals
The Distributed Web Crawler aims to:
- **Demonstrate parallelism and concurrency** by fetching multiple web pages simultaneously.
- **Implement multiprocessing** to handle multiple requests efficiently.
- **Utilize multithreading** for optimized web scraping and link extraction.
- **Enable interprocess communication (IPC)** for seamless data sharing between processes.
- **Implement distributed computing** by assigning tasks across multiple machines.
- **Facilitate internode communication** for better coordination between nodes.
- **Manage resources efficiently** using a task queue and avoid redundant crawling.
- **Create a scalable and extensible system** capable of handling large-scale web crawling.

## Features
- **Parallel Page Fetching** (Multiprocessing)
- **Concurrent Link Extraction** (Multithreading)
- **Master-Worker Architecture**: A master node assigns URLs to worker nodes (Task Distribution).
- **Interprocess Communication (IPC)**: Worker nodes share results using queues or shared memory.
- **Internode Communication**: Nodes exchange crawling results with each other.
- **Distributed Crawling**: Multiple machines work together to enhance performance.
- **Failure Recovery**: The system can resume crawling if a node crashes.
- **Scalability**: Additional worker nodes can be added to improve performance.
- **Data Analysis & Visualization**: Web page summary and analytics.

## Implementation Checklist
- [x] Web Scrapper Creation
- [x] Add Multithreading for web scraping and link extraction
- [ ]Summarize Recipes
- [ ]Implement Recovery for Failure
- [ ]Display Recipes on Website (linked)

## How We Will Demonstrate the Project
- Displaying a **web page with data insights** gathered from the web crawler.
- Summarizing extracted data in **structured formats**.
- Storing and analyzing data in a **database**.
- Visualizing information using **graphs and charts**.

## References
- [Cloudflare - What Is a Web Crawler?](https://www.cloudflare.com/learning/bots/what-is-a-web-crawler/)
- [GeeksforGeeks - What Is a Web Crawler and Where Is It Used?](https://www.geeksforgeeks.org/what-is-a-webcrawler-and-where-is-it-used/)
- [Elastic - Web Crawling Guide](https://www.elastic.co/what-is/web-crawler)
- [TechTarget - What Is a Web Crawler?](https://www.techtarget.com/)

---


