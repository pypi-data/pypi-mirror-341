# minakicoin/validators/transactions/structure.py

def is_valid_structure(tx) -> bool:
    """Validate the structure of a transaction (basic shape, not logic or crypto)."""

    if not hasattr(tx, "txid") or not tx.txid:
        print("❌ Missing or invalid txid")
        return False

    if not hasattr(tx, "inputs") or not isinstance(tx.inputs, list):
        print("❌ Missing or invalid inputs")
        return False

    if not hasattr(tx, "outputs") or not isinstance(tx.outputs, list):
        print("❌ Missing or invalid outputs")
        return False

    for i, txin in enumerate(tx.inputs):
        if not hasattr(txin, "txid") or not hasattr(txin, "index"):
            print(f"❌ Input #{i} is missing txid or index")
            return False
        if not hasattr(txin, "signature") or not hasattr(txin, "public_key"):
            print(f"❌ Input #{i} is missing signature or public key")
            return False

    for i, txout in enumerate(tx.outputs):
        if not hasattr(txout, "recipient") or not hasattr(txout, "amount"):
            print(f"❌ Output #{i} is missing recipient or amount")
            return False

    return True
