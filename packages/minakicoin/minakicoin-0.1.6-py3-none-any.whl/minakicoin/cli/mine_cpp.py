# minakicoin/cli/mine_cpp_block.py

import click
from minakicoin.services.cpp_mining_engine import mine_block_cpp

@click.command("mine-cpp")
@click.argument("miner_address")
def mine_block_cpp_cmd(miner_address):
    """Mine and insert a block using the C++ engine"""
    block = mine_block_cpp(miner_address)
    if block:
        click.echo(f"✅ Block #{block.index} mined and inserted")
    else:
        click.echo("❌ Failed to mine block")
