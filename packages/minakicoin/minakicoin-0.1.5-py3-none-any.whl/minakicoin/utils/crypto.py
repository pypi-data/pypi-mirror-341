# utils/crypto.py

import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


def generate_keypair():
    """Generate a new SECP256K1 keypair."""
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key) -> str:
    """Serialize a public key to base64 string."""
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    return base64.b64encode(pub_bytes).decode()


def serialize_private_key(private_key) -> str:
    """Serialize a private key to PEM string."""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode()


def deserialize_private_key(pem_str: str):
    """Deserialize PEM to private key object."""
    return serialization.load_pem_private_key(pem_str.encode(), password=None)


def deserialize_public_key(pub_b64: str):
    """Deserialize base64 to public key object."""
    pub_bytes = base64.b64decode(pub_b64)
    return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), pub_bytes)


def sign(data: str, private_key) -> str:
    """Sign data with private key. Returns hex signature."""
    signature = private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

# minakicoin/utils/crypto.py

import base64
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

def verify_signature(public_key_b64: str, signature_hex: str, message: str) -> bool:
    try:
        # Fix padding
        missing_padding = len(public_key_b64) % 4
        if missing_padding:
            public_key_b64 += '=' * (4 - missing_padding)

        pub_bytes = base64.b64decode(public_key_b64)
        if pub_bytes[0] == 0x04:
            pub_bytes = pub_bytes[1:]  # remove uncompressed prefix

        vk = VerifyingKey.from_string(pub_bytes, curve=SECP256k1)
        return vk.verify(bytes.fromhex(signature_hex), message.encode())

    except (BadSignatureError, Exception) as e:
        print(f"❌ Signature error: {e}")
        return False
