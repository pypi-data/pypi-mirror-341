# minakicoin/core/storage.py

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.block import Block
from ..models.transaction import Transaction
from ..models.utxo import UTXO
from ..models.wallet import Wallet


class IBlockStore(ABC):
    @abstractmethod
    def save_block(self, block: Block) -> None:
        pass

    @abstractmethod
    def get_block_by_index(self, index: int) -> Optional[Block]:
        pass

    @abstractmethod
    def get_latest_block(self) -> Optional[Block]:
        pass


class ITxStore(ABC):
    @abstractmethod
    def save_transaction(self, tx: Transaction) -> None:
        pass

    @abstractmethod
    def get_pending_transactions(self) -> List[Transaction]:
        pass


class IUTXOStore(ABC):
    @abstractmethod
    def get_utxos(self, address: str) -> List[UTXO]:
        pass

    @abstractmethod
    def save_utxos(self, utxos: List[UTXO]) -> None:
        pass


class IWalletStore(ABC):
    @abstractmethod
    def save_wallet(self, wallet: Wallet) -> None:
        pass

    @abstractmethod
    def load_wallet(self, name: str) -> Optional[Wallet]:
        pass
