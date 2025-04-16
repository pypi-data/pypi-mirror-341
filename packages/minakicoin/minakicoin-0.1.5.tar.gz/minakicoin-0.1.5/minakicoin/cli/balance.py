import click
from minakicoin.services.wallet_store import get_wallet
from minakicoin.services.utxo_store_sqlite import get_utxos
from minakicoin.services.mempool import load_mempool
from minakicoin.models.transactions import TxInput, TxOutput
import re

@click.command("balance")
@click.argument("input")
def wallet_balance(input):
    # Detect if input is an address (hex string) or a label
    is_address = bool(re.fullmatch(r"[a-f0-9]{64}", input))

    if is_address:
        address = input
        label = None
    else:
        wallet = get_wallet(input)
        if not wallet:
            click.echo(f"❌ Wallet '{input}' not found.")
            return
        address = wallet['address']
        label = input

    utxos = get_utxos(address)
    utxo_ids = {(u.txid, u.index) for u in utxos}

    # Load pending transactions
    mempool = load_mempool()
    pending_inputs = set()
    pending_outputs = []

    for tx in mempool:
        for i in tx.inputs:
            if isinstance(i, TxInput):
                pending_inputs.add((i.txid, i.index))
            elif isinstance(i, dict):
                pending_inputs.add((i.get("txid"), i.get("index")))

        for o in tx.outputs:
            if isinstance(o, TxOutput) and o.recipient == address:
                pending_outputs.append(o.amount)
            elif isinstance(o, dict) and o.get("recipient") == address:
                pending_outputs.append(float(o.get("amount", 0)))

    # UTXOs not used in pending TXs
    confirmed_utxos = [u for u in utxos if (u.txid, u.index) not in pending_inputs]
    confirmed_balance = sum(u.amount for u in confirmed_utxos)
    pending_balance = sum(pending_outputs)

    label_display = label if label else address
    click.echo(f"💰 Balance for {label_display}: {confirmed_balance:.1f} MINA (confirmed) + {pending_balance:.1f} MINA (pending) = {(confirmed_balance + pending_balance):.1f} MINA")
