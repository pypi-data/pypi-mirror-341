# modules/wallet/wallet.py

import os, json, hashlib
from minakicoin.modules.wallet.keys import ECKeypair

class Wallet:
    def __init__(self, name: str, path="wallets"):
        self.name = name
        self.path = os.path.join(path, f"{name}.json")
        self.keypair = ECKeypair()

        if os.path.exists(self.path):
            self.load()
        else:
            self.save()

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        data = self.keypair.to_dict()
        data["address"] = self.get_address()
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)
            self.keypair.from_dict(data)

    def get_address(self):
        pubkey = self.keypair.get_public_key()
        return "BC" + hashlib.sha256(pubkey.encode()).hexdigest()[:48]
