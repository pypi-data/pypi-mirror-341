# minakicoin/services/mining_engine.py

import time
import re
import uuid
from minakicoin.services.blockchain import get_blockchain, add_block
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos
from minakicoin.services.mempool import load_mempool, save_mempool
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxOutput
from minakicoin.services.block_validation import validate_block  # New passive validator import

BLOCK_REWARD = 50.0

def is_valid_address(address: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", address)) or (address and len(address) >= 16)

import uuid

def create_coinbase_transaction(miner_address: str) -> Transaction:
    coinbase_tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient=miner_address, amount=BLOCK_REWARD)],
        sender="COINBASE",
        recipient=miner_address,
        amount=BLOCK_REWARD,
        metadata=str(uuid.uuid4())  # 👈 include this if your txid is hash-based
    )
    coinbase_tx.txid = coinbase_tx.compute_txid()
    print(f"[💰] Coinbase TX created: {coinbase_tx.txid}")
    return coinbase_tx


def mine_block(miner_address: str):
    print(f"[⛏️ ] Mining block for: {miner_address}")

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
        if not tx.txid:
            tx.txid = tx.compute_txid()

        # 🚫 Skip if the transaction tries to spend the coinbase TX
        if any(inp.txid == coinbase_tx.txid for inp in tx.inputs):
            print(f"[🚫] TX {tx.txid} tries to spend coinbase — skipping.")
            continue

        print(f"[➡️ ] Including TX: {tx.txid}")
        included_txs.append(tx)  # ❗Don't spend UTXOs yet

    chain = get_blockchain()
    latest_block = chain[-1]
    block = Block(
        index=latest_block.index + 1,
        previous_hash=latest_block.hash,
        timestamp=int(time.time()),
        transactions=[coinbase_tx] + included_txs,
        nonce=0
    )

    block.mine()

    print(f"[🔎] Validating mined block #{block.index}...")
    from minakicoin.services.utxo_store_sqlite import get_all_utxos
    if not validate_block(block, get_all_utxos()):
        print(f"❌ Block #{block.index} failed validation and will not be added.")
        return None

    # ✅ Now safe to mark inputs as spent
    for tx in included_txs:
        spend_utxos(tx.inputs)

    add_block(block)
    print(f"[✔️] Block #{block.index} accepted: {block.hash}")

    add_utxos(coinbase_tx.txid, coinbase_tx.outputs)
    for tx in included_txs:
        add_utxos(tx.txid, tx.outputs)

    save_mempool(remaining)
    print(f"[🧹] Mempool updated. {len(remaining)} TXs remaining.")
    print(f"✅ Mined block #{block.index}: {block.hash}")
    return block
