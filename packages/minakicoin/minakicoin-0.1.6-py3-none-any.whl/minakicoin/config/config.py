# config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "minakicoin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "minakicoin_db"),
}

# minakicoin/config/config.py

import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="minakicoin",
        password="password",
        database="minakicoin_db"
    )

#BLOCK_INTERVAL = 180  # seconds (3 minutes)

# config/config.py
import os

CHAIN_DB = os.getenv("CHAIN_DB", "chain.db")
UTXO_DB = os.getenv("UTXO_DB", "utxo_store.db")
WALLET_DB = os.getenv("WALLET_DB", "wallets.db")
MEMPOOL_FILE = os.getenv("MEMPOOL_FILE", "mempool.json")

BLOCK_INTERVAL = 180  # seconds (3 minutes)
