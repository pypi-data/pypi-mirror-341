# minakicoin/services/utxo_store_sqlite.py

import sqlite3
import os
from minakicoin.models.utxo import UTXO
from minakicoin.config import config

DB_FILE = config.UTXO_DB

def ensure_db_initialized():
    """Create the utxos table if it doesn't exist"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS utxos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                txid TEXT NOT NULL,
                idx INTEGER NOT NULL,
                recipient TEXT NOT NULL,
                amount REAL NOT NULL,
                spent INTEGER DEFAULT 0
            );
        """)
        conn.commit()

# Auto-run this when module is imported
ensure_db_initialized()

def get_utxos(address: str) -> list[UTXO]:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT txid, idx, recipient, amount FROM utxos WHERE recipient = ? AND spent = 0", (address,))
        rows = c.fetchall()
        return [UTXO(txid=r[0], index=r[1], recipient=r[2], amount=r[3]) for r in rows]

def spend_utxos(inputs):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        for i in inputs:
            c.execute("UPDATE utxos SET spent = 1 WHERE txid = ? AND idx = ?", (i.txid, i.index))
        conn.commit()

def add_utxos_bk(txid: str, outputs):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        for idx, o in enumerate(outputs):
            c.execute("INSERT INTO utxos (txid, idx, recipient, amount) VALUES (?, ?, ?, ?)",
                      (txid, idx, o.recipient, o.amount))
        conn.commit()

def add_utxos(txid: str, outputs):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        for idx, o in enumerate(outputs):
            # 👇 Check if this exact UTXO already exists
            c.execute("SELECT 1 FROM utxos WHERE txid = ? AND idx = ?", (txid, idx))
            if c.fetchone():
                print(f"[⚠️] Skipping duplicate UTXO: {txid} [{idx}]")
                continue
            c.execute("INSERT INTO utxos (txid, idx, recipient, amount) VALUES (?, ?, ?, ?)",
                      (txid, idx, o.recipient, o.amount))
        conn.commit()
        print(f"[✅] add_utxos: Inserted {len(outputs)} outputs for TXID {txid}")

def get_all_utxos() -> dict:
    """Returns a dict of unspent UTXOs keyed by 'txid:index'"""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT txid, idx, recipient, amount FROM utxos WHERE spent = 0")
        rows = c.fetchall()
        return {f"{r[0]}:{r[1]}": UTXO(txid=r[0], index=r[1], recipient=r[2], amount=r[3]) for r in rows}
