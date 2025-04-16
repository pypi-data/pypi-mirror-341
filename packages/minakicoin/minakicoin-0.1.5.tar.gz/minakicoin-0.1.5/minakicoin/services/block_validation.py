# minakicoin/services/block_validation.py

from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction
from minakicoin.services.transaction_validation import validate_transaction

BLOCK_REWARD = 50.0  # Max allowed coinbase payout


def validate_block(block: Block, utxo_set: dict) -> bool:
    """
    Validates a single block against core rules:
    - Coinbase transaction rules
    - Transaction correctness
    - Hash integrity & Proof of Work
    - Double spending in block

    Returns True if valid, False if invalid
    """
    print(f"🔍 Validating block: {block.hash[:10]}...")

    # 1. Hash Integrity
    recalculated = block.calculate_hash()
    if block.hash != recalculated:
        print(f"⚠️  Hash mismatch: block hash = {block.hash}, recalculated = {recalculated}")
        return False

    # 2. Proof of Work
    if not block.hash.startswith("0000"):  # adjust difficulty as needed
        print(f"⚠️  Block does not meet difficulty target: {block.hash}")
        return False

    # 3. Coinbase Transaction Validity
    if not block.transactions or not isinstance(block.transactions[0], Transaction):
        print("⚠️  Missing or malformed coinbase transaction")
        return False

    coinbase_tx = block.transactions[0]

    if coinbase_tx.inputs:
        print("⚠️  Coinbase transaction should have no inputs")
        return False

    coinbase_output_total = sum(output.amount for output in coinbase_tx.outputs)
    if coinbase_output_total > BLOCK_REWARD:
        print(f"⚠️  Coinbase output exceeds reward: {coinbase_output_total} > {BLOCK_REWARD}")
        return False

    # 4. Validate Regular Transactions
    seen_inputs = set()
    for tx in block.transactions[1:]:
        if not validate_transaction(tx, utxo_set):
            print(f"⚠️  Transaction failed validation: {tx.txid}")
            return False

        for tx_input in tx.inputs:
            #key = f"{tx_input.txid}:{tx_input.output_index}"
            key = f"{tx_input.txid}:{tx_input.index}"
            if key in seen_inputs:
                print(f"⚠️  Double spend detected within block: {key}")
                return False
            seen_inputs.add(key)

    print("✅ Block passed full validation")
    return True
