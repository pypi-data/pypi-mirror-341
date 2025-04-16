# services/blockchain_store_sqlite.py

import sqlite3
import json
import os
from minakicoin.models.block import Block
from minakicoin.services.block_factory import create_genesis_block

DB_FILE = "chain.db"

def init_db():
    """Initializes the blockchain DB and inserts the genesis block if necessary."""
    first_time = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            idx INTEGER PRIMARY KEY,
            block_json TEXT NOT NULL
        )
    """)
    conn.commit()

    # Insert genesis block if the chain is empty
    c.execute("SELECT COUNT(*) FROM blocks")
    count = c.fetchone()[0]
    if count == 0:
        print("🪙 No blocks found. Creating Genesis block...")
        genesis = create_genesis_block()
        block_json = json.dumps(genesis.to_dict())
        c.execute("INSERT INTO blocks (idx, block_json) VALUES (?, ?)", (0, block_json))
        conn.commit()

    conn.close()

def save_chain(chain):
    """Overwrites the DB with a new chain."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM blocks")
    for i, block in enumerate(chain):
        block_json = json.dumps(block.to_dict())
        c.execute("INSERT INTO blocks (idx, block_json) VALUES (?, ?)", (i, block_json))
    conn.commit()
    conn.close()

def load_chain():
    """Loads the chain from the database."""
    init_db()  # ✅ Ensure DB is initialized
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT block_json FROM blocks ORDER BY idx ASC")
    rows = c.fetchall()
    conn.close()
    return [Block.from_dict(json.loads(row[0])) for row in rows]
