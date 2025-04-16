# minakicoin/services/transaction_validation.py

from minakicoin.models.transactions import Transaction
from minakicoin.validators.transactions.runner import run_all_validations

def validate_transaction(tx: Transaction, utxo_set: dict) -> bool:
    """
    Delegates to the modular validation pipeline.
    """
    print(f"🔎 Validating transaction via full pipeline: {tx.txid}")
    #return run_all_validations(tx, utxo_set)
    return run_all_validations(tx, utxo_set, public_key="")
