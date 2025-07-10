from flask import Flask, request, jsonify
import docker
import threading
import time
import requests
from consistent_hash import ConsistentHashRing

app = Flask(__name__)
client = docker.from_env()

ring = ConsistentHashRing(num_slots=1024, num_virtual_nodes=100)
replicas = {}  # Maps server_id -> container_name

DEFAULT_SERVERS = 3
NETWORK = "distributed-lab_net1"
IMAGE = "distributed-lab-server1"  # Adjust if needed

# Health check every 5 seconds
HEARTBEAT_INTERVAL = 5

@app.route("/home", methods=["GET"])
def route_request():
    request_id = str(time.time_ns())
    server_id = ring.get_server(request_id)
    if not server_id:
        return jsonify({"error": "No servers available"}), 503
    try:
        res = requests.get(f"http://{replicas[server_id]}:5000/home", timeout=2)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": f"Server {server_id} failed: {e}"}), 502

@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({"message": {"replicas": list(replicas.values())}})

@app.route("/add", methods=["POST"])
def add_servers():
    data = request.get_json()
    n = int(data.get("n", 0))
    hostnames = data.get("hostnames", [])
    added = []
    for i in range(n):
        sid = str(i + 1)
        hostname = hostnames[i] if i < len(hostnames) else f"Server{i+1}"
        if sid not in replicas:
            ring.add_server(sid)
            replicas[sid] = hostname
            added.append(hostname)
    return jsonify({"message": f"Added: {added}"}), 200

@app.route("/rm", methods=["DELETE"])
def remove_servers():
    data = request.get_json()
    n = int(data.get("n", 0))
    hostnames = data.get("hostnames", [])
    removed = []
    if not hostnames:
        # remove first n
        to_remove = list(replicas.items())[:n]
    else:
        to_remove = [(sid, name) for sid, name in replicas.items() if name in hostnames]

    for sid, name in to_remove:
        ring.remove_server(sid)
        removed.append(name)
        replicas.pop(sid)
    return jsonify({"message": f"Removed: {removed}"}), 200

def monitor():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        dead = []
        for sid, hostname in list(replicas.items()):
            try:
                res = requests.get(f"http://{hostname}:5000/heartbeat", timeout=2)
                if res.status_code != 200:
                    dead.append((sid, hostname))
            except:
                dead.append((sid, hostname))

        for sid, hostname in dead:
            print(f"[MONITOR] Removing dead server {hostname}")
            ring.remove_server(sid)
            replicas.pop(sid)

if __name__ == "__main__":
    # Register pre-running servers launched by docker-compose
    for i in range(1, DEFAULT_SERVERS + 1):
        sid = str(i)
        replicas[sid] = f"Server{sid}"
        ring.add_server(sid)

    threading.Thread(target=monitor, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)