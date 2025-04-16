# minakicoin/cli/utxos.py

import os
import sqlite3
import click

@click.command("utxos")
@click.argument("label")
def wallet_utxos(label):
    """List UTXOs for a given wallet label"""

    wallet_db = os.path.join(os.getcwd(), "wallets.db")
    utxo_db = os.path.join(os.getcwd(), "utxo_store.db")

    # 1. Lookup wallet address by label
    try:
        conn = sqlite3.connect(wallet_db)
        cursor = conn.cursor()
        cursor.execute("SELECT address FROM wallets WHERE label = ?", (label,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            click.echo(f"❌ Wallet label not found: {label}")
            return

        address = row[0]
    except Exception as e:
        click.echo(f"❌ Error accessing wallets.db: {e}")
        return

    # 2. Query UTXOs by address
    try:
        conn = sqlite3.connect(utxo_db)
        cursor = conn.cursor()
        cursor.execute("SELECT txid, idx, amount FROM utxos WHERE recipient = ?", (address,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            click.echo(f"💸 No UTXOs found for {label} ({address})")
            return

        click.echo(f"🔍 UTXOs for {label} ({address}):")
        for i, (txid, idx, amount) in enumerate(results, start=1):
            click.echo(f"  #{i}: TXID={txid}, Index={idx}, Amount={amount}")
    except Exception as e:
        click.echo(f"❌ Error accessing utxo_store.db: {e}")
