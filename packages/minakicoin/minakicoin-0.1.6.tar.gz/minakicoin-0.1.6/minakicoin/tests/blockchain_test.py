# tests/blockchain_test.py

import time
from minakicoin.models.transactions import Transaction, TxOutput
from minakicoin.models.block import Block
from minakicoin.services.blockchain import (
    load_persisted_chain,
    get_blockchain,
    get_latest_block,
    add_block
)

def test_blockchain_load():
    print("[🧠] Loading blockchain from chain.db...")
    load_persisted_chain()
    chain = get_blockchain()
    print(f"[✅] Blockchain has {len(chain)} blocks")

def test_adding_block():
    print("[🧠] Loading blockchain from chain.db...")
    load_persisted_chain()
    last_block = get_latest_block()

    # Create a dummy transaction
    tx = Transaction(
        sender="test_sender",
        recipient="test_recipient",
        amount=1.23,
        inputs=[],
        outputs=[TxOutput("test_recipient", 1.23)]
    )
    tx.txid = tx.compute_txid()

    # Build new block
    new_block = Block(
        index=last_block.index + 1,
        previous_hash=last_block.hash,
        timestamp=int(time.time()),
        transactions=[tx],
        nonce=0
    )

    # Mine the block to meet difficulty
    new_block.mine()

    print(f"[🧪] Stored hash:       {new_block.hash}")
    print(f"[🧪] Recalculated hash: {new_block.compute_hash()}")
    print(f"[🧪] Starts with '0000': {new_block.hash.startswith('0000')}")

    # Add block to chain
    add_block(new_block)
    print(f"[✅] Block #{new_block.index} added successfully")

if __name__ == "__main__":
    test_blockchain_load()
    test_adding_block()
