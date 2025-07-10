import bisect
import hashlib

class ConsistentHashRing:
    def __init__(self, num_slots=1024, num_virtual_nodes=100):
        self.num_slots = num_slots
        self.num_virtual_nodes = num_virtual_nodes
        self.ring = []
        self.nodes = {}
        self.server_map = {}  # slot -> server_id

    def _hash(self, key):
        h = hashlib.sha256(key.encode()).hexdigest()
        return int(h, 16) % self.num_slots

    def _get_virtual_node_key(self, server_id, replica_id):
        return f"{server_id}-{replica_id}"

    def add_server(self, server_id):
        if server_id in self.nodes:
            return
        self.nodes[server_id] = []
        for i in range(self.num_virtual_nodes):
            key = self._get_virtual_node_key(server_id, i)
            slot = self._hash(key)
            if slot in self.server_map:
                continue
            bisect.insort(self.ring, slot)
            self.server_map[slot] = server_id
            self.nodes[server_id].append(slot)

    def remove_server(self, server_id):
        if server_id not in self.nodes:
            return
        for slot in self.nodes[server_id]:
            self.ring.remove(slot)
            del self.server_map[slot]
        del self.nodes[server_id]

    def get_server(self, request_id):
        if not self.ring:
            return None
        slot = self._hash(str(request_id))
        idx = bisect.bisect(self.ring, slot)
        if idx == len(self.ring):
            idx = 0
        return self.server_map[self.ring[idx]]