# models/utxo.py

from dataclasses import dataclass

@dataclass
class UTXO:
    txid: str
    index: int
    recipient: str
    amount: float
