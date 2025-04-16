# minakicoin/core/miner.py

from abc import ABC, abstractmethod
from typing import Optional
from .blockchain import IBlock


class IMiner(ABC):
    @abstractmethod
    def mine_block(self) -> Optional[IBlock]:
        """Attempt to mine a block. Returns block if successful, else None."""
        pass

    @abstractmethod
    def set_mining_address(self, address: str) -> None:
        """Sets the wallet address to receive rewards."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Gracefully stops mining."""
        pass
