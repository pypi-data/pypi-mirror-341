# minakicoin/services/cpp_mining_engine.py

import os
import time
import json
import uuid
import subprocess
from minakicoin.services.blockchain import get_blockchain, add_block
from minakicoin.services.mempool import load_mempool, save_mempool
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos
from minakicoin.services.block_validation_cpp import validate_block_cpp
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxOutput

BLOCK_REWARD = 50.0

def mine_block_cpp(miner_address: str):
    print(f"[⚙️ ] Starting C++ mining pipeline for: {miner_address}")

    # ✅ Build coinbase transaction
    coinbase_tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient=miner_address, amount=BLOCK_REWARD)],
        sender="COINBASE",
        recipient=miner_address,
        amount=BLOCK_REWARD,
        metadata=str(uuid.uuid4())
    )
    coinbase_tx.txid = coinbase_tx.compute_txid()

    # ✅ Get mempool transactions
    raw_mempool = load_mempool(raw=True)
    txs_raw = raw_mempool[:5]
    included_txs = [Transaction.from_dict(tx["data"]) for tx in txs_raw]

    # ✅ Get blockchain context
    chain = get_blockchain()
    latest_block = chain[-1]
    new_index = latest_block.index + 1
    timestamp = int(time.time())
    previous_hash = latest_block.hash

    # ✅ Create tx_summary (for C++ mining hash consistency)
    tx_summary = "+".join([coinbase_tx.txid] + [tx.txid for tx in included_txs])

    cpp_input_block = {
        "index": new_index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "tx_summary": tx_summary
    }

    # ✅ Write mining input file
    with open("cpp_input_block.json", "w") as f:
        json.dump(cpp_input_block, f, indent=2)

    # ✅ Execute RandomX C++ miner
    try:
        subprocess.run(["./cpp/randomx_miner"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ C++ miner failed: {e}")
        return None

    # ✅ Parse mined output
    if not os.path.exists("cpp_mined_block.json"):
        print("❌ Mined block file not found.")
        return None

    with open("cpp_mined_block.json", "r") as f:
        mined = json.load(f)

    # ✅ Construct mined block
    block = Block(
        index=new_index,
        previous_hash=previous_hash,
        timestamp=mined.get("mined_timestamp", timestamp),
        transactions=[coinbase_tx] + included_txs,
        nonce=mined["nonce"],
        hash=mined["hash"]
    )
    block.tx_summary = tx_summary  # required by validate_block_cpp

    # ✅ Validate using C++-compatible validator
    print(f"[🔎] Validating mined block #{block.index}...")
    if not validate_block_cpp(block):
        print(f"❌ Block #{block.index} failed validation and will not be added.")
        return None

    # ✅ Finalize block
    for tx in included_txs:
        spend_utxos(tx.inputs)
        add_utxos(tx.txid, tx.outputs)

    add_utxos(coinbase_tx.txid, coinbase_tx.outputs)
    add_block(block)

    save_mempool(raw_mempool[5:])
    print(f"✅ Mined block #{block.index}: {block.hash}")
    return block
