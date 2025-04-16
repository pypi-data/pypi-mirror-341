# minakicoin/p2p_node/routes/broadcast.py

from fastapi import APIRouter, Request
import httpx
from minakicoin.models.transactions import Transaction
from minakicoin.models.block import Block
from minakicoin.services.mempool import add_tx
from minakicoin.services.blockchain import add_block, get_blockchain
from minakicoin.p2p_node.state import known_peers

router = APIRouter()

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
