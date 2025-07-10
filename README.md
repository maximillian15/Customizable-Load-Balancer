# Customizable-Load-Balancer
A scalable load balancing system built with Flask, Docker, and Python. Supports consistent hashing, failure detection, dynamic scaling, and request analysis — ideal for distributed systems labs or microservices learning.

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

## Clone the Project
<pre> ```bash docker build -t distributed-lab-server1 ./server docker run -d --name Server1 --network distributed-lab_net1 -e SERVER_ID=1 distributed-lab-server1 ``` </pre>

