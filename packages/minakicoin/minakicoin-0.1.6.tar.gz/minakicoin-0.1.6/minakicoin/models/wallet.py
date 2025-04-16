# models/wallet.py

import hashlib
import json
import os
from decimal import Decimal

from minakicoin.models.transactions import Transaction, TxInput, TxOutput
from minakicoin.services.utxo_store import get_utxos, spend_utxos

# Save all wallets to a consistent location
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALLET_STORE = os.path.join(PROJECT_ROOT, "wallets.json")

class Wallet:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address()

    def get_address(self):
        return "BC" + hashlib.sha256(self.name.encode()).hexdigest()[:48]

    def sign(self, data):
        return hashlib.sha256((self.name + json.dumps(data)).encode()).hexdigest()

    def create_transaction(self, to, amount):
        utxos = get_utxos(self.address)
        selected = []
        total = 0.0

        for u in utxos:
            selected.append(u)
            total += u.amount
            if total >= amount:
                break

        if total < amount:
            raise Exception("❌ Insufficient funds.")

        inputs = [TxInput(txid=u.txid, index=u.index) for u in selected]
        outputs = [TxOutput(recipient=to, amount=amount)]

        # Add change output if needed
        if total > amount:
            outputs.append(TxOutput(recipient=self.address, amount=total - amount))

        tx = Transaction(
            inputs=inputs,
            outputs=outputs,
            sender=self.address,
            recipient=to,
            amount=amount
        )
        tx.txid = tx.compute_txid()

        for txin in tx.inputs:
            txin.signature = self.sign(tx.txid)

        return tx

    def save(self):
        wallets = Wallet.load_all()
        wallets[self.name] = self.address
        with open(WALLET_STORE, "w") as f:
            json.dump(wallets, f, indent=2)

    @staticmethod
    def load_all():
        if not os.path.exists(WALLET_STORE):
            return {}
        with open(WALLET_STORE, "r") as f:
            return json.load(f)

    @staticmethod
    def list_wallets():
        return Wallet.load_all()
