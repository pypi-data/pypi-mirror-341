# models/block.py

from dataclasses import dataclass
from typing import List
import json
import hashlib
from .transactions import Transaction

@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: int
    transactions: List[Transaction]
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict(include_sig=True) for tx in self.transactions],
            "nonce": self.nonce
        }
        encoded = json.dumps(data, sort_keys=True)
        return hashlib.sha256(encoded.encode()).hexdigest()

    def mine(self, difficulty=6):
        prefix = "0" * difficulty
        print(f"[⚙️ ] Mining block with difficulty: {difficulty}")
        nonce = 0
        while True:
            self.nonce = nonce
            hashed = self.compute_hash()
            if hashed.startswith(prefix):
                self.hash = hashed
                print(f"[✅] Block mined: {self.hash}")
                break
            nonce += 1

    def is_valid(self, difficulty=6):
        recalculated = self.compute_hash()
        starts_with = recalculated.startswith("0" * difficulty)
        print(f"[🧪] Stored hash:       {self.hash}")
        print(f"[🧪] Recalculated hash: {recalculated}")
        print(f"[🧪] Starts with '0000': {starts_with}")
        return self.hash == recalculated and starts_with

    def to_dict(self, include_hash=True):
        data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        if include_hash:
            data["hash"] = self.hash
        return data

    @staticmethod
    def from_dict(data):
        txs = [
            tx if isinstance(tx, Transaction) else Transaction.from_dict(tx)
            for tx in data["transactions"]
        ]
        return Block(
            index=data["index"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            transactions=txs,
            nonce=data["nonce"],
            hash=data.get("hash", "")
        )

    @staticmethod
    def from_row(row):
        idx, hash_, prev_hash, nonce, timestamp, txs_json = row
        txs = json.loads(txs_json)
        txs = [Transaction.from_dict(tx) for tx in txs]
        return Block(
            index=idx,
            previous_hash=prev_hash,
            nonce=nonce,
            timestamp=timestamp,
            transactions=txs,
            hash=hash_
        )

    def serialize_transactions(self):
        return json.dumps([tx.to_dict() for tx in self.transactions])

    def calculate_hash(self):
        """
        Returns the SHA-256 hash of the block header and transactions.
        """
        block_content = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
