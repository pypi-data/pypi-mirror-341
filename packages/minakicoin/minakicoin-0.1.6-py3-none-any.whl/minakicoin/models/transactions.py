# models/transactions.py

from dataclasses import dataclass, field
from typing import List, Union
import hashlib
import json
from ecdsa import SigningKey, SECP256k1
import base64


@dataclass
class TxInput:
    txid: str
    index: int
    signature: str = ""
    public_key: str = ""  # 👈 Add this


    @staticmethod
    def from_dict(data: dict) -> "TxInput":
        return TxInput(
            txid=data.get("txid", ""),
            index=data.get("index", 0),
            signature=data.get("signature", ""),
            public_key=data.get("public_key", "")

       )


@dataclass
class TxOutput:
    recipient: str
    amount: float

    @staticmethod
    def from_dict(data: dict) -> "TxOutput":
        return TxOutput(
            recipient=data.get("recipient", ""),
            amount=float(data.get("amount", 0))
        )


@dataclass
class Transaction:
    inputs: List[Union[TxInput, dict]]
    outputs: List[Union[TxOutput, dict]]
    sender: str
    recipient: str
    amount: float
    metadata: str = ""  # 👈 Add this line
    txid: str = field(default_factory=lambda: "")

    #def compute_txid(self) -> str:
    #    data = json.dumps(self.to_dict(include_sig=False), sort_keys=True)
    #    return hashlib.sha256(data.encode()).hexdigest()

    def compute_txid(self) -> str:
        data = json.dumps(self.to_dict(include_sig=False), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self, include_sig=True) -> dict:
        return {
            "txid": self.txid,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "metadata": self.metadata,  # 👈 Add this line
            "inputs": [
                self._safe_input_dict(i, include_sig) for i in self.inputs
            ],
            "outputs": [
                self._safe_output_dict(o) for o in self.outputs
            ],
        }

    def _safe_input_dict(self, i, include_sig):
        if isinstance(i, TxInput):
            return vars(i) if include_sig else {"txid": i.txid, "index": i.index}
        elif isinstance(i, dict):
            return i
        else:
            raise ValueError("Invalid TX input type")

    def _safe_output_dict(self, o):
        if isinstance(o, TxOutput):
            return vars(o)
        elif isinstance(o, dict):
            return o
        else:
            raise ValueError("Invalid TX output type")

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        inputs = [TxInput.from_dict(i) for i in data.get("inputs", [])]
        outputs = [TxOutput.from_dict(o) for o in data.get("outputs", [])]
        return Transaction(
            inputs=inputs,
            outputs=outputs,
            sender=data.get("sender", ""),
            recipient=data.get("recipient", ""),
            amount=float(data.get("amount", 0)),
            txid=data.get("txid", "")
        )

    def compute_signature_message(self) -> str:
        input_refs = "".join([f"{i.txid}:{i.index}" for i in self.inputs if isinstance(i, TxInput)])
        output_data = "".join([f"{o.recipient}:{o.amount}" for o in self.outputs if isinstance(o, TxOutput)])
        return f"{input_refs}->{output_data}"


    from ecdsa import SigningKey, SECP256k1
    import base64

    def sign(self, private_key_hex: str):
        """Signs the transaction inputs with a private key"""
        try:
            sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
            vk = sk.get_verifying_key()

            # base64-encode uncompressed pubkey
            pub_bytes = b'\x04' + vk.to_string()
            public_key_b64 = base64.b64encode(pub_bytes).decode()

            message = self.compute_signature_message()
            signature = sk.sign(message.encode()).hex()

            for tx_input in self.inputs:
                if isinstance(tx_input, TxInput):
                    tx_input.signature = signature
                    tx_input.public_key = public_key_b64

        except Exception as e:
            raise ValueError(f"Signing failed: {e}")

