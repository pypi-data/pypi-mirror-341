# minakicoin/modules/network/peer_store.py

import json
import os

PEER_FILE = "data/peers.json"

def load_peers():
    if not os.path.exists(PEER_FILE):
        return []
    with open(PEER_FILE, "r") as f:
        return json.load(f)

def save_peer(url):
    peers = load_peers()
    if not any(peer.get("url") == url for peer in peers):
        peers.append({"url": url})
        with open(PEER_FILE, "w") as f:
            json.dump(peers, f, indent=2)
