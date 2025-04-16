# minakicoin/validators/transactions/utxo_check.py

def inputs_exist_in_utxo(tx, utxo_set: dict) -> bool:
    """Check if all inputs refer to valid UTXOs."""

    for txin in tx.inputs:
        key = f"{txin.txid}:{txin.index}"
        if key not in utxo_set:
            print(f"❌ Input not found in UTXO set: {key}")
            return False

    return True
