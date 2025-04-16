# minakicoin/cli/create.py
import click
from minakicoin.services.wallet_store import init_wallet_db, create_wallet as create_wallet_fn

@click.command(name="create")
@click.argument("label")
def create_wallet(label):
    """Create a new wallet"""
    init_wallet_db()
    result = create_wallet_fn(label)
    if "error" in result:
        click.echo(f"❌ Error: {result['error']}")
    else:
        click.echo(f"✅ Wallet '{label}' created")
        click.echo(f"🔐 Address: {result['address']}")
