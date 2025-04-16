# modules/wallet/keys.py

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature

class ECKeypair:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def sign(self, data: str) -> str:
        sig = self.private_key.sign(
            data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return sig.hex()

    def to_dict(self):
        return {
            "private_key": self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
        }

    def from_dict(self, data):
        self.private_key = serialization.load_pem_private_key(
            data["private_key"].encode(),
            password=None
        )
        self.public_key = self.private_key.public_key()
