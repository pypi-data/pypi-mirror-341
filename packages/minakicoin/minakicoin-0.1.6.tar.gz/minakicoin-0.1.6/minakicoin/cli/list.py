# minakicoin/cli/list.py

import click
from minakicoin.services.wallet_store import list_wallets as get_wallets

@click.command(name="list")
def list_wallets():
    """List all wallets"""
    wallets = get_wallets()
    if not wallets:
        click.echo("No wallets found.")
    else:
        for w in wallets:
            click.echo(f"🔖 {w['label']} - {w['address']}")
