# core/blockchain.py

import time
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxInput, TxOutput
from minakicoin.services.blockchain_store_sqlite import load_chain, save_chain, init_db

init_db()

def get_chain():
    return load_chain()

def get_latest_block():
    chain = load_chain()
    return chain[-1] if chain else generate_genesis_block()

def generate_genesis_block():
    print("[🌱] Generating genesis block")

    genesis_tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient="GENESIS", amount=0)],
        sender="GENESIS",
        recipient="GENESIS",
        amount=0
    )
    genesis_tx.txid = genesis_tx.compute_txid()

    genesis_block = Block(
        index=0,
        previous_hash="0" * 64,
        timestamp=int(time.time()),
        transactions=[genesis_tx],
        nonce=0
    )
    genesis_block.mine()
    save_chain([genesis_block])
    return genesis_block

def add_block(new_block: Block):
    chain = load_chain()
    latest = chain[-1] if chain else generate_genesis_block()

    if new_block.previous_hash != latest.hash:
        raise ValueError("❌ Invalid previous hash")
    if not new_block.is_valid():
        raise ValueError("❌ Invalid block")

    chain.append(new_block)
    save_chain(chain)
    print(f"[✔️] Block #{new_block.index} added to chain")

def get_block_by_index(idx: int):
    chain = load_chain()
    return chain[idx] if 0 <= idx < len(chain) else None
