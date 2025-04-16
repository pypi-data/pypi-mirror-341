import sqlite3
from ecdsa import SigningKey, SECP256k1
import hashlib
from minakicoin.config import config

from importlib.resources import files

DB_FILE = config.WALLET_DB

def init_wallet_db():
    schema_path = files("minakicoin.config").joinpath("wallet_schema.sql")
    with sqlite3.connect(DB_FILE) as conn:
        with open(schema_path, "r") as f:
            conn.executescript(f.read())
        conn.commit()

def create_wallet(label: str):
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    private_key = sk.to_string().hex()
    public_key = vk.to_string().hex()
    address = hashlib.sha256(vk.to_string()).hexdigest()

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO wallets (label, public_key, private_key, address) VALUES (?, ?, ?, ?)",
                         (label, public_key, private_key, address))
            conn.commit()
        return {
            "label": label,
            "address": address,
            "public_key": public_key
        }
    except sqlite3.IntegrityError:
        return {"error": "Wallet label already exists"}

def list_wallets():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT label, address FROM wallets").fetchall()
        return [{"label": r[0], "address": r[1]} for r in rows]

def get_wallet(label: str):
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute("SELECT * FROM wallets WHERE label = ?", (label,)).fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "label": row[1],
            "public_key": row[2],
            "private_key": row[3],
            "address": row[4],
            "created_at": row[5]
        }
