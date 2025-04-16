# minakicoin/services/mining_multiproc_engine.py

import time
import uuid
import re
from multiprocessing import Process, Event, Queue, current_process
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxOutput
from minakicoin.services.blockchain import get_blockchain, add_block
from minakicoin.services.block_validation import validate_block
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos, get_all_utxos
from minakicoin.services.mempool import load_mempool, save_mempool

BLOCK_REWARD = 50.0
DIFFICULTY = 6

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

def mine_worker(base_block_dict, difficulty, start_nonce, step, result_queue, found_event):
    prefix = "0" * difficulty
    nonce = start_nonce
    base_block = Block.from_dict(base_block_dict)

    while not found_event.is_set():
        block = Block.from_dict(base_block_dict)
        block.nonce = nonce
        hash_attempt = block.compute_hash()

        if nonce % 50000 == 0:
            print(f"[🧠 {current_process().name}] Nonce={nonce} → {hash_attempt[:12]}", end="\r")

        if hash_attempt.startswith(prefix):
            block.hash = hash_attempt
            found_event.set()
            result_queue.put(block)
            print(f"\n✅ [{current_process().name}] Found! Nonce={nonce} Hash={hash_attempt}")
            return
        nonce += step

def mine_block_multiproc(miner_address: str, num_processes: int):
    print(f"🚀 Starting multi-process mining for {miner_address} using {num_processes} processes")

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

    found_event = Event()
    result_queue = Queue()
    processes = []

    for i in range(num_processes):
        p = Process(
            target=mine_worker,
            args=(base_block.to_dict(include_hash=False), DIFFICULTY, i, num_processes, result_queue, found_event),
            name=f"Proc-{i}"
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if result_queue.empty():
        print("❌ No block found by any process.")
        return None

    block = result_queue.get()

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
