# minakicoin/cli/address.py
import click
from minakicoin.services.wallet_store import get_wallet

@click.command("address")
@click.argument("label")
def wallet_address(label):
    """Show address of a wallet"""
    wallet = get_wallet(label)
    if not wallet:
        click.echo("❌ Wallet not found.")
    else:
        click.echo(f"📬 Address for '{label}': {wallet['address']}")
