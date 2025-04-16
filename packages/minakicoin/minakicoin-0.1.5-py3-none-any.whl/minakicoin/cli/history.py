# minakicoin/cli/history.py
import click
import sqlite3
import json
from minakicoin.services.wallet_store import get_wallet

@click.command("history")
@click.argument("label")
def wallet_history(label):
    """Show TX history for wallet"""
    wallet = get_wallet(label)
    if not wallet:
        click.echo("❌ Wallet not found.")
        return

    address = wallet['address']
    conn = sqlite3.connect("chain.db")
    cursor = conn.cursor()
    cursor.execute("SELECT block_json FROM blocks")
    rows = cursor.fetchall()
    conn.close()

    txs = []
    for row in rows:
        block = json.loads(row[0])
        for tx in block.get("transactions", []):
            for out in tx["outputs"]:
                if out["recipient"] == address:
                    txs.append((tx["txid"], out["amount"], "IN"))
            for inp in tx["inputs"]:
                if inp.get("signature") and address in inp["signature"]:  # simple check
                    txs.append((tx["txid"], "-", "OUT"))

    if not txs:
        click.echo("📭 No transaction history found.")
        return

    for tx in txs:
        click.echo(f"📦 {tx[0]} | {tx[2]} | Amount: {tx[1]}")
