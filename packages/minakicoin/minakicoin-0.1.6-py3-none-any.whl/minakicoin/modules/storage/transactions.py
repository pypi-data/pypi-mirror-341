# minakicoin/modules/storage/transactions.py

from minakicoin.config.config import get_db
from minakicoin.models.transaction import Transaction

def save_transaction(tx: Transaction, confirmed=True):
    conn = get_db()
    cursor = conn.cursor()

    # Save to transactions table
    cursor.execute("""
        INSERT INTO transactions (txid, sender, recipient, amount, tx_type, confirmed, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (tx.txid, tx.sender, tx.recipient, tx.amount, tx.tx_type, confirmed))

    # Save inputs
    for i, txin in enumerate(tx.inputs):
        cursor.execute("""
            INSERT INTO tx_inputs (txid, input_txid, input_index, signature)
            VALUES (%s, %s, %s, %s)
        """, (tx.txid, txin.txid, txin.index, txin.signature))

    # Save outputs
    for i, out in enumerate(tx.outputs):
        cursor.execute("""
            INSERT INTO tx_outputs (txid, output_index, recipient, amount)
            VALUES (%s, %s, %s, %s)
        """, (tx.txid, i, out.recipient, out.amount))

    conn.commit()
    cursor.close()
    conn.close()
