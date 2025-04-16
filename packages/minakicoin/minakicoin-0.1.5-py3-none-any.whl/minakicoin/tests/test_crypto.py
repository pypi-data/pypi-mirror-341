# tests/test_crypto.py

from minakicoin.utils import crypto


def test_key_generation_and_signing():
    priv, pub = crypto.generate_keypair()
    priv_pem = crypto.serialize_private_key(priv)
    pub_b64 = crypto.serialize_public_key(pub)

    # Deserialize to test round-trip
    priv2 = crypto.deserialize_private_key(priv_pem)
    pub2 = crypto.deserialize_public_key(pub_b64)

    data = "test-message"
    signature = crypto.sign(data, priv2)

    assert crypto.verify_signature(data, signature, pub_b64)
