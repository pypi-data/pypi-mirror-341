from minakicoin.models.transactions import Transaction
from minakicoin.utils.crypto import verify_signature

def verify_tx_signatures(tx: Transaction) -> bool:
    """Verify all input signatures in a transaction."""
    message = tx.compute_signature_message()

    for i, tx_input in enumerate(tx.inputs):
        if not hasattr(tx_input, "signature") or not hasattr(tx_input, "public_key"):
            print(f"❌ Input #{i} missing signature or public_key")
            return False

        if not verify_signature(tx_input.public_key, tx_input.signature, message):
            print(f"❌ Invalid signature for input #{i}")
            return False

    return True
