# minakicoin/main.py

import click

# Import CLI groups
from minakicoin.cli.wallet import wallet
from minakicoin.cli.p2p import p2p

@click.group()
def cli():
    """Minakicoin CLI"""
    pass

cli.add_command(wallet)
cli.add_command(p2p)

if __name__ == "__main__":
    cli()
