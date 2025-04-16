# p2p_node/routes_mining.py

from fastapi import APIRouter, Request
from minakicoin.models.transactions import Transaction
from minakicoin.services.mempool import add_tx, get_pending, remove_txs
from minakicoin.services.blockchain import get_latest_block, add_block
from minakicoin.models.block import Block
from minakicoin.p2p_node.state import known_peers
import time
import httpx

router = APIRouter()

@router.post("/tx/send")
async def submit_tx(request: Request):
    data = await request.json()
    tx = Transaction.from_dict(data.get("tx"))
    success = add_tx(tx)
    return {"status": "success" if success else "duplicate", "txid": tx.txid}

@router.post("/mine")
async def mine_block():
    mempool = get_pending()
    if not mempool:
        return {"error": "No transactions to mine"}

    latest = get_latest_block()
    new_block = Block(
        index=latest.index + 1,
        previous_hash=latest.hash,
        timestamp=int(time.time()),
        transactions=mempool
    )
    new_block.mine()
    add_block(new_block)
    remove_txs(mempool)

    print(f"[⛏️] Mined and added block #{new_block.index}: {new_block.hash}")

    # Broadcast to peers
    for peer in known_peers:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"{peer}/broadcast/block", json={"block": new_block.to_dict()})
        except Exception:
            print(f"[⚠️] Could not broadcast to {peer}")

    return {"status": "block mined", "hash": new_block.hash}
