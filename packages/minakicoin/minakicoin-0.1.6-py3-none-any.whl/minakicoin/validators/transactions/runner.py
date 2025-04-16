from minakicoin.validators.transactions.structure import is_valid_structure
from minakicoin.validators.transactions.signatures import verify_tx_signatures
from minakicoin.validators.transactions.utxo_check import inputs_exist_in_utxo
from minakicoin.validators.transactions.rules import validate_transaction_rules

def run_all_validations(tx, utxo_set, public_key: str = "") -> bool:
    """Run all validators in a chain."""
    
    if not is_valid_structure(tx):
        return False

    if not verify_tx_signatures(tx):
        return False

    if not inputs_exist_in_utxo(tx, utxo_set):
        return False

    if not validate_transaction_rules(tx, utxo_set):
        return False

    print("✅ Transaction is valid")
    return True
