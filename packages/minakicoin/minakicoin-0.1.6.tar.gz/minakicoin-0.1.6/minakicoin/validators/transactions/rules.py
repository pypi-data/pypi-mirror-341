# minakicoin/validators/transactions/rules.py

def validate_transaction_rules(tx, utxo_set: dict) -> bool:
    """Ensure total input ≥ total output."""

    total_input = 0
    for txin in tx.inputs:
        key = f"{txin.txid}:{txin.index}"
        utxo = utxo_set.get(key)
        if not utxo:
            continue
        #total_input += utxo["amount"]
        total_input += utxo.amount

    total_output = sum([o.amount for o in tx.outputs])

    if total_output > total_input:
        print(f"❌ Output exceeds input ({total_output} > {total_input})")
        return False

    return True
