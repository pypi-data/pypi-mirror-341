# p2p_node/state.py
import os
from minakicoin.services.peer_store import load_peers

# 🔁 Load known peers from file
known_peers = load_peers()


# Absolute path to the known_peers.json at the project root
PEERS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "known_peers.json")

def get_known_peers():
    """Dynamically load known peers from disk."""
    try:
        with open(PEERS_FILE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
