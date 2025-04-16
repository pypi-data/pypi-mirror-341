# services/mempool.py

import os
import json
import time
from typing import List
from minakicoin.models.transactions import Transaction
from minakicoin.services.utxo_store_sqlite import get_all_utxos

MEMPOOL_FILE = "mempool.json"
TX_TTL_SECONDS = 300  # 5 minutes

def _now():
    return int(time.time())

def load_mempool(raw=False) -> List[dict]:
    if not os.path.exists(MEMPOOL_FILE):
        return []
    try:
        with open(MEMPOOL_FILE, "r") as f:
            data = json.load(f)
            return data if raw else [Transaction.from_dict(tx["data"]) for tx in data]
    except Exception as e:
        print(f"[❌] Failed to load mempool: {e}")
        return []

def save_mempool(mempool: List[dict]):
    try:
        with open(MEMPOOL_FILE, "w") as f:
            json.dump(mempool, f, indent=2)
    except Exception as e:
        print(f"[❌] Failed to save mempool: {e}")

def _mempool_inputs() -> set:
    """Return a set of 'txid:index' currently used in the mempool"""
    seen_inputs = set()
    mempool = load_mempool(raw=True)
    for tx_raw in mempool:
        tx = Transaction.from_dict(tx_raw["data"])
        for tx_input in tx.inputs:
            seen_inputs.add(f"{tx_input.txid}:{tx_input.index}")
    return seen_inputs

def add_tx(tx: Transaction):
    mempool = load_mempool(raw=True)

    # 1. Reject duplicate TXID
    for item in mempool:
        if item["data"]["txid"] == tx.txid:
            print(f"[⚠️] TX {tx.txid} already exists in mempool")
            return False

    # 2. Check if all TX inputs exist in the UTXO set
    utxo_set = get_all_utxos()
    for tx_input in tx.inputs:
        key = f"{tx_input.txid}:{tx_input.index}"
        if key not in utxo_set:
            print(f"[🚫] TX {tx.txid} rejected — input {key} not found in UTXO set (already spent or invalid)")
            return False

    # 3. Check if inputs already used in mempool
    used_inputs = _mempool_inputs()
    for tx_input in tx.inputs:
        key = f"{tx_input.txid}:{tx_input.index}"
        if key in used_inputs:
            print(f"[🚫] TX {tx.txid} rejected — input {key} already used in mempool")
            return False

    # 4. Accept TX
    mempool.append({
        "data": tx.to_dict(),
        "timestamp": _now()
    })
    save_mempool(mempool)
    print(f"[🌀] TX {tx.txid} added to mempool")
    return True

def get_pending(limit: int = 5) -> List[Transaction]:
    mempool = load_mempool(raw=True)
    return [
        Transaction.from_dict(tx["data"])
        for tx in mempool
        if _now() - tx["timestamp"] <= TX_TTL_SECONDS
    ][:limit]

def remove_txs(txs: List[Transaction]):
    txids_to_remove = [tx.txid for tx in txs]
    mempool = load_mempool(raw=True)
    updated = [tx for tx in mempool if tx["data"]["txid"] not in txids_to_remove]
    save_mempool(updated)

def cleanup_mempool():
    mempool = load_mempool(raw=True)
    filtered = [tx for tx in mempool if _now() - tx["timestamp"] <= TX_TTL_SECONDS]
    if len(filtered) != len(mempool):
        save_mempool(filtered)
        print(f"[🧹] Cleaned expired TXs from mempool")

def clear():
    if os.path.exists(MEMPOOL_FILE):
        os.remove(MEMPOOL_FILE)
