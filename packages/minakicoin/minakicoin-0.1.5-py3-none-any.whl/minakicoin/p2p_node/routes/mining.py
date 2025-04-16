# minakicoin/p2p_node/routes/mining.py
from fastapi import APIRouter, Query
from minakicoin.services.mining_engine import mine_block
#from fastapi import APIRouter
import httpx
from minakicoin.p2p_node.state import known_peers

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "alive"}

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


@router.get("/mine")
async def mine(miner: str):
    block = mine_block(miner)
    if not block:
        return {"error": "Failed to mine block"}

    # Broadcast to peers after mining
    for peer in known_peers:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{peer}/broadcast/block",
                    json={"block": block.to_dict()}
                )
        except Exception as e:
            print(f"[⚠️] Failed to broadcast to {peer}: {e}")

    return {
        "index": block.index,
        "hash": block.hash,
        "tx_count": len(block.transactions),
        "timestamp": block.timestamp
    }
