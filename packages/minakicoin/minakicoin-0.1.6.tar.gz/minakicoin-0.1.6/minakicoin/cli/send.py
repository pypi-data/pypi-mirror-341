# minakicoin/cli/send.py

import click
import httpx
from minakicoin.services.wallet_store import get_wallet
from minakicoin.services.utxo_store_sqlite import get_utxos
from minakicoin.models.transactions import Transaction, TxInput, TxOutput
from minakicoin.p2p_node.state import known_peers
from minakicoin.services.mempool import add_tx

@click.command("send")
@click.argument("from_label")
@click.argument("to_address")
@click.argument("amount", type=float)
def send(from_label, to_address, amount):
    """Send coins from one wallet to another"""
    sender_wallet = get_wallet(from_label)
    if not sender_wallet:
        click.echo("❌ Sender wallet not found.")
        return

    sender_address = sender_wallet['address']
    utxos = get_utxos(sender_address)

    selected = []
    total = 0
    for utxo in utxos:
        selected.append(utxo)
        total += utxo.amount
        if total >= amount:
            break

    if total < amount:
        click.echo(f"❌ Not enough balance. You have {total} MINA.")
        return

    change = total - amount
    inputs = [TxInput(txid=u.txid, index=u.index, signature="") for u in selected]
    outputs = [TxOutput(recipient=to_address, amount=amount)]
    if change > 0:
        outputs.append(TxOutput(recipient=sender_address, amount=change))

    tx = Transaction(
        inputs=inputs,
        outputs=outputs,
        sender=sender_address,
        recipient=to_address,
        amount=amount
    )
    tx.sign(sender_wallet['private_key'])
    tx.txid = tx.compute_txid()

    if not add_tx(tx):
        click.echo("❌ TX rejected — possible double spend or invalid input.")
        return

    # If added to mempool, now broadcast to peers
    for peer in known_peers:
        try:
            httpx.post(f"{peer}/broadcast/tx", json={"tx": tx.to_dict()})
        except Exception:
            pass

    click.echo(f"✅ Sent {amount} MINA from '{from_label}' to {to_address}")
    click.echo(f"🔐 TXID: {tx.txid}")
    click.echo("📡 TX broadcasted to peers.")
