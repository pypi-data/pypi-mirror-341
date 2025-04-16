# minakicoin/tests/test_wallet_keys.py

from minakicoin.modules.wallet.wallet import SimpleWallet
from minakicoin.modules.wallet.keys import ECKeypair
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import base64

def test_keypair_and_signing():
    wallet = SimpleWallet()
    message = "test-message"

    signature = wallet.sign_transaction(message)
    pubkey_b64 = wallet.export_public_key()

    # Decode pubkey
    pubkey_bytes = base64.b64decode(pubkey_b64)
    pubkey = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), pubkey_bytes)

    # Verify signature
    try:
        pubkey.verify(bytes.fromhex(signature), message.encode(), ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        assert False, "Signature could not be verified"

    # Ensure the address is derived and looks okay
    address = wallet.get_address()
    assert address.startswith("BC") and len(address) >= 20
