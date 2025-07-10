# Customizable-Load-Balancer
A scalable load balancing system built with Flask, Docker, and Python. Supports consistent hashing, failure detection, dynamic scaling, and request analysis — ideal for distributed systems labs or microservices learning.

## Overview

This project involves building a load balancer that efficiently distributes requests among multiple server replicas using consistent hashing. It automatically manages the number of replicas, scaling up by spawning new instances in case of server failures. Docker containerization simplifies deployment and management.

## Purpose

The load balancer aims to handle increasing client loads by efficiently distributing requests across server replicas. This improves resource utilization and throughput in applications like distributed caching, databases, and network traffic systems.


## Coding Environment

- **OS**: Ubuntu 20.04 LTS or above
- **Docker**: Version 20.10.23 or above
- **Languages**: Python (preferred), C++, Java, or your choice

## Project Structure

distributed-lab/
│
├── load_balancer/
│ ├── balancer.py 
│ └── consistent_hash.py 
│
├── server/
│ └── server.py 
│
├── test_runner.py 
├── docker-compose.yml 
├── Makefile 
└── README.md 


# Installation

1. **Install Docker:**

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
2. **Install Docker-Compose:**

```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

3. **Run The Project**

### Clone Project 

```bash
git clone https://github.com/yourusername/distributed-lab.git
cd distributed-lab
```

### Start the project

```bash
make up
```

### Run tests

```bash
make a1, make a2, make a3, make a4 
```

## Testing and Performance Analysis

### Experiment 1: Load Distribution

- Launch 10,000 asynchronous requests on 3 server containers.
- Record the number of requests handled by each server and plot a bar chart.
- Expected Outcome: Even distribution of load among server instances.

![image](https://github.com/maximillian15/Customizable-Load-Balancer/blob/main/images/a1%20test2.png)





