import asyncio
import aiohttp
import matplotlib.pyplot as plt
import json
from collections import defaultdict

BASE_URL = "http://localhost:5000"

async def send_request(session, endpoint="/home"):
    async with session.get(f"{BASE_URL}{endpoint}") as response:
        try:
            data = await response.json()
            return data.get("message", "")
        except:
            return "<error>"

async def run_requests(n=10000):
    results = defaultdict(int)
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(n)]
        responses = await asyncio.gather(*tasks)
        for msg in responses:
            print(">>", msg)
            if "Server" in msg:
                results[msg] += 1
    return results

def plot_bar(data, title):
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.xticks(rotation=45)
    plt.title(title)
    plt.ylabel("Request Count")
    plt.tight_layout()
    plt.show()

def plot_line(x_vals, y_vals):
    plt.plot(x_vals, y_vals, marker='o')
    plt.xlabel("Number of Servers (N)")
    plt.ylabel("Average Load per Server")
    plt.title("Scalability of Load Balancer")
    plt.grid(True)
    plt.show()

# ---------- Task A1 ----------
async def task_a1():
    print("Running Task A1: Load Distribution (N=3)...")
    result = await run_requests()

    if not result:
        print("No valid server responses received.")
    else:
        for server, count in result.items():
            print(f"{server}: {count} requests")


    plot_bar(result, "Load Distribution Across 3 Servers")

# ---------- Task A2 ----------
async def task_a2():
    print("Running Task A2: Scalability Test (N=2 to 6)...")
    averages = []
    x_range = list(range(2, 7))

    for n in x_range:
        # Reset servers
        await reset_servers(n)

        result = await run_requests()
        avg = sum(result.values()) / len(result)
        averages.append(avg)

    plot_line(x_range, averages)

# Helper to reset server replicas via API
async def reset_servers(n):
    import requests
    print(f"> Resetting replicas to N = {n}...")
    requests.delete(f"{BASE_URL}/rm", json={"n": 100, "hostnames": []})  # remove all
    hostnames = [f"Server{i}" for i in range(1, n+1)]
    requests.post(f"{BASE_URL}/add", json={"n": n, "hostnames": hostnames})

# ---------- Task A3 ----------
async def task_a3():
    print("Running Task A3: Failure Detection and Recovery...")
    import requests
    from time import sleep

    # Get current replicas
    response = requests.get(f"{BASE_URL}/rep").json()
    initial_replicas = response['message']['replicas']
    kill_target = initial_replicas[0]
    print(f"> Simulating failure of {kill_target}...")

    # Kill one container
    container_id = kill_target
    os.system(f"docker stop {container_id}")  # simulate failure

    print("> Waiting 10 seconds for auto-recovery...")
    sleep(10)

    updated = requests.get(f"{BASE_URL}/rep").json()
    print("Updated replicas:", updated["message"]["replicas"])

# ---------- Task A4 ----------
async def task_a4():
    print("Task A4 requires modifying the hash functions in consistent_hash.py.")
    print("You can replace the hash functions with alternatives like:")
    print(" - H(i) = (3 * i + 41) % M")
    print(" - Φ(i, j) = (7 * i + 11 * j + 31) % M")
    print("Then re-run task_a1 and task_a2 for comparison.")

if __name__ == "__main__":
    import sys
    import os

    tasks = {
        "a1": task_a1,
        "a2": task_a2,
        "a3": task_a3,
        "a4": task_a4
    }

    if len(sys.argv) < 2 or sys.argv[1] not in tasks:
        print("Usage: python test_runner.py [a1|a2|a3|a4]")
        exit(1)

    asyncio.run(tasks[sys.argv[1]]())