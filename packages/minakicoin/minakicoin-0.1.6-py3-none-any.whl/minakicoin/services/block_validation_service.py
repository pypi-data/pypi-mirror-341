# minakicoin/services/block_validation_service.py

from minakicoin.models.block import BlockModel
from minakicoin.models.transaction import TransactionModel
from typing import Dict


def validate_block_structure(block: BlockModel) -> bool:
    """Basic sanity checks on block structure."""
    if not block.transactions or not isinstance(block.transactions, list):
        return False
    return True


def validate_coinbase_transaction(tx: TransactionModel, expected_reward: float = 50.0) -> bool:
    """Validates the first transaction in the block (coinbase)."""
    if tx.inputs:
        return False  # Coinbase should have no inputs
    total_output = sum(output.amount for output in tx.outputs)
    return total_output <= expected_reward


def validate_transaction(tx: TransactionModel, utxo_set: Dict[str, float]) -> bool:
    """Validates transaction by checking its inputs and outputs."""
    input_total = 0.0
    used_inputs = set()

    for txin in tx.inputs:
        ref = f"{txin.tx_id}:{txin.output_index}"
        if ref not in utxo_set:
            return False  # UTXO doesn't exist
        if ref in used_inputs:
            return False  # Double spend in same block
        used_inputs.add(ref)
        input_total += utxo_set[ref]

    output_total = sum(output.amount for output in tx.outputs)
    return input_total >= output_total


def validate_block(block: BlockModel, utxo_set: Dict[str, float], expected_reward: float = 50.0) -> bool:
    """Top-level validation for a single block."""
    if not validate_block_structure(block):
        return False

    # Validate coinbase
    coinbase_tx = block.transactions[0]
    if not validate_coinbase_transaction(coinbase_tx, expected_reward):
        return False

    # Validate all other transactions
    for tx in block.transactions[1:]:
        if not validate_transaction(tx, utxo_set):
            return False

    return True
