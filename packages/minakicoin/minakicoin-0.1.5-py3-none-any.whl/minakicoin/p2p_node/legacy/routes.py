# p2p_node/routes.py

from fastapi import APIRouter, Request
from minakicoin.p2p_node.state import known_peers
from minakicoin.services.blockchain import add_block, get_blockchain
from minakicoin.services.blockchain_sync import sync_blockchain_from_peer
from minakicoin.services.mempool import add_tx
from minakicoin.models.block import Block
from minakicoin.models.transactions import Transaction
from minakicoin.services.peer_store import save_peers

import sqlite3
import json
import httpx

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "alive"}

@router.get("/peers")
async def get_peers():
    return {"known_peers": known_peers}

@router.post("/register")
async def register_peer(request: Request):
    data = await request.json()
    peer_url = data.get("peer")
    if peer_url and peer_url not in known_peers:
        known_peers.append(peer_url)
        save_peers(known_peers)
        print(f"[🔗] New peer registered: {peer_url}")
    return {"peers": known_peers}

@router.post("/peer/forget")
async def forget_peer(request: Request):
    data = await request.json()
    peer = data.get("peer")
    if peer in known_peers:
        known_peers.remove(peer)
        save_peers(known_peers)
        print(f"[🗑️] Peer removed: {peer}")
        return {"removed": peer}
    return {"error": "peer not found"}

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

from minakicoin.models.transactions import Transaction
from minakicoin.services.mempool import add_tx

@router.post("/broadcast/tx")
async def receive_tx(request: Request):
    data = await request.json()
    tx_data = data.get("tx")

    if not tx_data:
        return {"error": "No TX received"}

    tx = Transaction.from_dict(tx_data)
    result = add_tx(tx)

    if result:
        print(f"[🌀] TX {tx.txid} received and added to mempool")
    else:
        print(f"[⚠️] TX {tx.txid} already exists in mempool")

    return {"status": "received", "txid": tx.txid}

@router.post("/broadcast/block")
async def receive_block(request: Request):
    data = await request.json()
    block_data = data.get("block")
    block = Block.from_dict(block_data)

    # 🚫 Check if block already exists in chain
    current_chain = get_blockchain()
    if any(b.hash == block.hash for b in current_chain):
        return {"status": "block already exists"}

    try:
        add_block(block)
        print(f"[📦] Block #{block.index} accepted: {block.hash}")

        for peer in known_peers:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(f"{peer}/broadcast/block", json={"block": block.to_dict()})
            except Exception:
                print(f"[⚠️] Could not forward block to {peer}")

        return {"status": "block accepted"}
    except Exception as e:
        print(f"[❌] Block rejected: {e}")
        return {"status": "block rejected", "error": str(e)}

@router.get("/heartbeat")
async def heartbeat():
    live_peers = []
    for peer in known_peers:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{peer}/ping", timeout=2)
                if res.status_code == 200:
                    live_peers.append(peer)
        except Exception:
            pass
    return {"live_peers": live_peers}

@router.post("/sync/blockchain")
async def sync_blockchain_stub():
    print("[📡] Blockchain sync requested.")
    return {"blockchain": "not implemented"}

@router.post("/sync/mempool")
async def sync_mempool_stub():
    print("[🧠] Mempool sync requested.")
    return {"mempool": "not implemented"}
