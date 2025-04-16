# minakicoin/core/consensus.py

from abc import ABC, abstractmethod
from typing import Any
from .blockchain import IBlock


class IConsensus(ABC):
    @abstractmethod
    def is_valid_block(self, block: IBlock, previous_block: IBlock) -> bool:
        """Check whether a block is valid under the consensus rules."""
        pass

    @abstractmethod
    def meets_difficulty(self, block: IBlock) -> bool:
        """Checks whether the block meets the consensus difficulty."""
        pass

    @abstractmethod
    def calculate_difficulty(self, last_block: IBlock) -> int:
        """Calculates the difficulty for the next block."""
        pass
