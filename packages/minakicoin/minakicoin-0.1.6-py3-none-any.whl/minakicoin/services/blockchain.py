from minakicoin.services.blockchain_store_sqlite import (
    load_chain,
    save_chain,
    init_db
)

from minakicoin.models.block import Block
from minakicoin.models.transactions import TxOutput
from minakicoin.services.mempool import remove_txs
from minakicoin.services.utxo_store_sqlite import spend_utxos, add_utxos

init_db()

def get_blockchain():
    return load_chain()

def get_latest_block():
    chain = load_chain()
    return chain[-1] if chain else None

def add_block(block: Block):
    chain = load_chain()
    chain.append(block)
    save_chain(chain)

    for tx in block.transactions:
        if tx.sender != "COINBASE":
            spend_utxos(tx.inputs)

        outputs = []
        for o in tx.outputs:
            if isinstance(o, dict):
                outputs.append(TxOutput.from_dict(o))
            else:
                outputs.append(o)

        add_utxos(tx.txid, outputs)

    # Remove mined TXs from mempool
    txs_to_remove = [tx for tx in block.transactions if tx.sender != "COINBASE"]
    remove_txs(txs_to_remove)

    print(f"[🔄] UTXOs updated for Block #{block.index}: {block.hash}")
