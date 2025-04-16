from dataclasses import dataclass

@dataclass
class BlockHeader:
    index: int
    hash: str
    previous_hash: str
    timestamp: int
    nonce: int

    @staticmethod
    def from_dict(data: dict) -> "BlockHeader":
        return BlockHeader(
            index=data["index"],
            hash=data["hash"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            nonce=data["nonce"]
        )
