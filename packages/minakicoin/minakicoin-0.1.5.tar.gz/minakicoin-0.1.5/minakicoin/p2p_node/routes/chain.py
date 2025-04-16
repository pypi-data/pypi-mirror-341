from fastapi import APIRouter, Request
import sqlite3, json
from minakicoin.services.blockchain_sync import sync_blockchain_from_peer
from minakicoin.services.blockchain_store_sqlite import load_chain
from minakicoin.services.blockchain import get_blockchain

router = APIRouter()

@router.get("/chain")
async def chain():
    try:
        conn = sqlite3.connect("chain.db")
        cursor = conn.cursor()
        cursor.execute("SELECT block_json FROM blocks ORDER BY idx ASC")
        rows = cursor.fetchall()
        conn.close()
        return {"chain": [json.loads(row[0]) for row in rows]}
    except Exception as e:
        return {"error": str(e)}

@router.get("/chain/rawdb")
async def get_chain_directly():
    return await chain()

@router.post("/sync/from-peer")
async def trigger_sync(request: Request):
    data = await request.json()
    peer = data.get("peer")
    if not peer:
        return {"error": "Missing peer URL"}
    await sync_blockchain_from_peer(peer)
    return {"status": f"Synced from {peer}"}

@router.get("/headers")
def get_headers():
#    chain = load_chain()
    chain = get_blockchain() 
    return [{
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "nonce": block.nonce,
    } for block in chain]
