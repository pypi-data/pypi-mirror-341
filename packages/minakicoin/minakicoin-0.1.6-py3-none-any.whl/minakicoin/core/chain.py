# core/chain.py

import time
from typing import List
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_tx = Transaction(
            inputs=[],
            outputs=[],
            sender="GENESIS",
            recipient="GENESIS",
            amount=0.0,
            txid="0" * 64
        )
        genesis_block = Block(
            index=0,
            previous_hash="0" * 64,
            timestamp=int(time.time()),
            transactions=[genesis_tx],
            nonce=0
        )
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block: Block) -> bool:
        latest = self.get_latest_block()

        if new_block.previous_hash != latest.hash:
            print("❌ Invalid previous hash")
            return False
        if new_block.index != latest.index + 1:
            print("❌ Invalid block index")
            return False
        if new_block.hash != new_block.compute_hash():
            print("❌ Invalid hash")
            return False

        self.chain.append(new_block)
        print(f"✅ Block #{new_block.index} added")
        return True

    def is_valid_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                return False
            if current.hash != current.compute_hash():
                return False

        return True

    def replace_chain_if_valid(self, new_chain: List[Block]) -> bool:
        if len(new_chain) <= len(self.chain):
            return False
        temp_chain = Blockchain()
        temp_chain.chain = new_chain
        if not temp_chain.is_valid_chain():
            return False
        self.chain = new_chain
        return True

    def to_list(self) -> List[dict]:
        return [block.to_dict() for block in self.chain]

    def from_list(self, blocks: List[dict]):
        self.chain = [Block.from_dict(b) for b in blocks]
