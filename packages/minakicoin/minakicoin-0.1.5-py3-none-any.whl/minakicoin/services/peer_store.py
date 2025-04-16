# services/peer_store.py

import json
import os

PEERS_FILE = "known_peers.json"

def load_peers():
    if not os.path.exists(PEERS_FILE):
        return []
    with open(PEERS_FILE, "r") as f:
        return json.load(f)

def save_peers(peers):
    with open(PEERS_FILE, "w") as f:
        json.dump(peers, f, indent=2)
