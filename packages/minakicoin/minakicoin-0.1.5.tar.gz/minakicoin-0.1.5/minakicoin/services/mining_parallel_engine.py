# minakicoin/services/mining_parallel_engine.py

import time
import re
import uuid
import threading
import sys
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxOutput
from minakicoin.services.blockchain import get_blockchain, add_block
from minakicoin.services.block_validation import validate_block
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos, get_all_utxos
from minakicoin.services.mempool import load_mempool, save_mempool

BLOCK_REWARD = 50.0
found_flag = threading.Event()
progress_lock = threading.Lock()

def is_valid_address(address: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", address)) or (address and len(address) >= 16)

def create_coinbase_transaction(miner_address: str) -> Transaction:
    coinbase_tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient=miner_address, amount=BLOCK_REWARD)],
        sender="COINBASE",
        recipient=miner_address,
        amount=BLOCK_REWARD,
        metadata=str(uuid.uuid4())
    )
    coinbase_tx.txid = coinbase_tx.compute_txid()
    print(f"[💰] Coinbase TX created: {coinbase_tx.txid}")
    return coinbase_tx

def mine_thread(base_block: Block, thread_id: int, step: int, result_block: list, difficulty: int):
    nonce = thread_id
    prefix = "0" * difficulty
    last_display = 0

    while not found_flag.is_set():
        block = Block.from_dict(base_block.to_dict(include_hash=False))
        block.nonce = nonce
        hash_attempt = block.compute_hash()

        # Update status every 10k
        if nonce - last_display >= 10000:
            with progress_lock:
                print(f"[🧵 T{thread_id}] Nonce: {nonce:<10} → {hash_attempt[:12]}", end="\r")
            last_display = nonce

        if hash_attempt.startswith(prefix):
            found_flag.set()
            block.hash = hash_attempt
            result_block[0] = block
            with progress_lock:
                print(f"\n✅ [T{thread_id}] BLOCK FOUND: Nonce={nonce} Hash={hash_attempt}")
            return

        nonce += step

def mine_block_parallel(miner_address: str, num_threads: int):
    print(f"🚀 Starting multi-threaded mining for {miner_address} using {num_threads} threads")

    if not is_valid_address(miner_address):
        print("❌ Invalid miner address")
        return None

    coinbase_tx = create_coinbase_transaction(miner_address)
    raw_mempool = load_mempool(raw=True)
    txs_raw = raw_mempool[:5]
    remaining = raw_mempool[5:]
    included_txs = []

    for tx_raw in txs_raw:
        tx = Transaction.from_dict(tx_raw["data"])
        if any(inp.txid == coinbase_tx.txid for inp in tx.inputs):
            continue
        included_txs.append(tx)

    chain = get_blockchain()
    latest_block = chain[-1]
    base_block = Block(
        index=latest_block.index + 1,
        previous_hash=latest_block.hash,
        timestamp=int(time.time()),
        transactions=[coinbase_tx] + included_txs,
        nonce=0
    )

    difficulty = 6  # <- pulled from the Block model’s default, or could make it dynamic
    result_block = [None]
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=mine_thread, args=(base_block, i, num_threads, result_block, difficulty))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    found_flag.clear()

    block = result_block[0]
    if not block:
        print("❌ No thread mined a valid block.")
        return None

    print(f"[🔍] Validating block #{block.index} with hash {block.hash}...")
    if not validate_block(block, get_all_utxos()):
        print("❌ Block failed validation")
        return None

    for tx in included_txs:
        spend_utxos(tx.inputs)
        add_utxos(tx.txid, tx.outputs)

    add_utxos(coinbase_tx.txid, coinbase_tx.outputs)
    add_block(block)
    save_mempool(remaining)

    print(f"✅ Final block #{block.index} accepted: {block.hash}")
    return block
