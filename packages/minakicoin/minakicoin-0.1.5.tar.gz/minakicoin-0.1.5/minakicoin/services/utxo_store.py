# services/utxo_store.py

import json
import os
from typing import List, Dict
from minakicoin.models.utxo import UTXO
from minakicoin.models.transactions import TxInput, TxOutput

UTXO_FILE = "utxo_store.json"
utxo_set: Dict[str, List[UTXO]] = {}

def load_utxos():
    global utxo_set
    if os.path.exists(UTXO_FILE):
        with open(UTXO_FILE, "r") as f:
            raw = json.load(f)
            utxo_set = {
                k: [UTXO(**u) for u in v]
                for k, v in raw.items()
            }
            print(f"[📥] Loaded {sum(len(v) for v in utxo_set.values())} UTXOs from disk")
    else:
        utxo_set = {}
        print("[📂] No existing UTXO store found")

def save_utxos():
    with open(UTXO_FILE, "w") as f:
        json.dump({
            k: [u.__dict__ for u in v]
            for k, v in utxo_set.items()
        }, f, indent=2)
        print(f"[💾] Saved UTXOs to {UTXO_FILE}")

def get_utxos(address: str) -> List[UTXO]:
    return utxo_set.get(address, [])

def add_utxos(txid: str, outputs: List[TxOutput]):
    for index, output in enumerate(outputs):
        utxo = UTXO(txid=txid, index=index, recipient=output.recipient, amount=output.amount)
        utxo_set.setdefault(output.recipient, []).append(utxo)
        print(f"[➕] UTXO added: {utxo}")
    save_utxos()

def spend_utxos(inputs: List[TxInput]):
    for txin in inputs:
        for address, utxos in utxo_set.items():
            before = len(utxos)
            utxo_set[address] = [
                u for u in utxos if not (u.txid == txin.txid and u.index == txin.index)
            ]
            after = len(utxo_set[address])
            if before != after:
                print(f"[💸] UTXO spent: {txin}")
    save_utxos()
