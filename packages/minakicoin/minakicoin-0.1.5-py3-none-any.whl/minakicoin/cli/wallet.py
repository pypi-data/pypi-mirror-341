# minakicoin/cli/wallet.py

import click

# Create the wallet CLI group
@click.group()
def wallet():
    """Wallet-related commands"""
    pass

# Import and add individual subcommands
from minakicoin.cli.create import create_wallet
from minakicoin.cli.address import wallet_address
from minakicoin.cli.balance import wallet_balance
from minakicoin.cli.send import send
from minakicoin.cli.mine import mine
from minakicoin.cli.list import list_wallets
from minakicoin.cli.history import wallet_history
#from minakicoin.cli.mine_cpp import mine_cpp
#from minakicoin.cli.mine_cpp import mine_block_cpp_cmd as mine_cpp
from minakicoin.cli.mine_parallel import mine_parallel
from minakicoin.cli.mine_multiproc import mine_multiproc  # ✅ ← NEW
from minakicoin.cli.mine_gpu import mine_gpu
from minakicoin.cli.utxos import wallet_utxos

wallet.add_command(mine_gpu)
wallet.add_command(mine_parallel)
#wallet.add_command(mine_cpp)
wallet.add_command(create_wallet)
wallet.add_command(wallet_address)
wallet.add_command(wallet_balance)
wallet.add_command(send)
wallet.add_command(mine)
wallet.add_command(list_wallets)
wallet.add_command(wallet_history)
wallet.add_command(mine_multiproc)  # ✅ ← NEW
wallet.add_command(wallet_utxos)
