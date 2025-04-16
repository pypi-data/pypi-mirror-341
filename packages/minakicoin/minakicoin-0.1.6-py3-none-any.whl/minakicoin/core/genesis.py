# minakicoin/core/genesis.py

import time
import hashlib
import json

GENESIS_BLOCK = {
    "index_height": 0,
    "previous_hash": "0" * 64,
    "merkle_root": "GENESIS_MERKLE",
    "nonce": 0,
    "difficulty": 4,
    "transactions": [],
    "timestamp": 0,
}

def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def create_genesis_block():
    block_data = GENESIS_BLOCK.copy()
    block_data["hash"] = compute_hash(block_data)
    return block_data
