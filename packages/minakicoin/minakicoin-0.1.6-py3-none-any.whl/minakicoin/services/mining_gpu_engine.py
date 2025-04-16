# minakicoin/services/mining_gpu_engine.py

import time
import uuid
import json
import numpy as np
from hashlib import sha256

from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxOutput
from minakicoin.services.blockchain import get_blockchain, add_block
from minakicoin.services.block_validation import validate_block
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos, get_all_utxos
from minakicoin.services.mempool import load_mempool, save_mempool

# --- CUDA check ---
HAS_CUDA = True
try:
    import pycuda.autoinit
    import pycuda.driver as drv
    from pycuda.compiler import SourceModule
except ImportError:
    HAS_CUDA = False


FIXED_DIFFICULTY = 5  # Hardcoded since Block model has no 'difficulty'
TARGET_PREFIX = "0" * FIXED_DIFFICULTY
MAX_ATTEMPTS = 1_000_000
BATCH_SIZE = 1024


def create_coinbase_tx(miner_address: str) -> Transaction:
    tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient=miner_address, amount=50)],
        sender="COINBASE",
        recipient=miner_address,
        amount=50,
        metadata=str(uuid.uuid4())
    )
    tx.txid = tx.compute_txid()
    print(f"[💰] Coinbase TX created: {tx.txid}")
    return tx


def mine_block_gpu(miner_address: str):
    if not HAS_CUDA:
        print("❌ CUDA is not available on this machine.")
        print("👉 Please install NVIDIA CUDA drivers and PyCUDA, or use `mining_multiproc_engine.py` for CPU mining.")
        return None

    print(f"🚀 Starting GPU mining for {miner_address}")
    print(f"[⚙️ ] Target hash prefix: {TARGET_PREFIX}")

    chain = get_blockchain()
    prev_block = chain[-1]

    mempool = load_mempool(raw=True)
    included = mempool[:5]
    remaining = mempool[5:]

    transactions = [create_coinbase_tx(miner_address)]
    for item in included:
        tx = Transaction.from_dict(item['data'])
        transactions.append(tx)

    block = Block(
        index=prev_block.index + 1,
        previous_hash=prev_block.hash,
        timestamp=int(time.time()),
        transactions=transactions,
        nonce=0
    )

    mod = SourceModule("""
    __global__ void generate_nonces(int *nonces, int start) {
        int idx = threadIdx.x + blockIdx.x * blockDim.x;
        nonces[idx] = start + idx;
    }
    """)
    generate_nonces = mod.get_function("generate_nonces")
    nonces_gpu = np.zeros(BATCH_SIZE, dtype=np.int32)

    for start in range(0, MAX_ATTEMPTS, BATCH_SIZE):
        generate_nonces(drv.Out(nonces_gpu), np.int32(start), block=(BATCH_SIZE,1,1), grid=(1,1))
        for n in nonces_gpu:
            block.nonce = int(n)
            h = block.compute_hash()
            if h.startswith(TARGET_PREFIX):
                block.hash = h
                print(f"[✅] Found valid nonce: {block.nonce} → {block.hash}")
                if validate_block(block, get_all_utxos()):
                    add_block(block)
                    for tx in transactions[1:]:
                        spend_utxos(tx.inputs)
                        add_utxos(tx.txid, tx.outputs)
                    add_utxos(transactions[0].txid, transactions[0].outputs)
                    save_mempool(remaining)
                    print(f"[🎉] Block #{block.index} successfully mined and added!")
                    return block
                else:
                    print(f"[❌] Block hash matched but failed validation.")
        print(f"[❌] Tried batch starting at nonce {start}, no match.")

    print("❌ GPU failed to find valid nonce within max attempts.")
    return None
