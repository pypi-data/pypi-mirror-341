# core/chain_store.py

import sqlite3
from minakicoin.models.block import Block

DB_FILE = "chain_store.db"

class ChainStore:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    idx INTEGER PRIMARY KEY,
                    hash TEXT,
                    prev_hash TEXT,
                    nonce INTEGER,
                    timestamp REAL,
                    txs TEXT
                )
            """)

    def save_block(self, block: Block):
        with self.conn:
            self.conn.execute("""
                INSERT INTO blocks (idx, hash, prev_hash, nonce, timestamp, txs)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                block.index,
                block.hash,
                block.previous_hash,
                block.nonce,
                block.timestamp,
                block.serialize_transactions()
            ))

    def get_latest_block(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM blocks ORDER BY idx DESC LIMIT 1")
        row = cur.fetchone()
        return Block.from_row(row) if row else None

    def get_block_by_index(self, idx: int):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM blocks WHERE idx = ?", (idx,))
        row = cur.fetchone()
        return Block.from_row(row) if row else None

    def get_chain(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM blocks ORDER BY idx")
        rows = cur.fetchall()
        return [Block.from_row(r) for r in rows]

    def clear(self):
        with self.conn:
            self.conn.execute("DELETE FROM blocks")
