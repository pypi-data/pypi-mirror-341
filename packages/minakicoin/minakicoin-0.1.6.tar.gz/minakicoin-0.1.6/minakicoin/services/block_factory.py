# services/block_factory.py

import time
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction, TxInput, TxOutput

def create_genesis_block():
    genesis_tx = Transaction(
        inputs=[],
        outputs=[TxOutput(recipient="GENESIS", amount=0)],
        sender="GENESIS",
        recipient="GENESIS",
        amount=0,
        txid="genesis_tx"
    )

    return Block(
        index=0,
        previous_hash="0" * 64,
        transactions=[genesis_tx],
        timestamp=int(time.time()),
        nonce=0
    )
