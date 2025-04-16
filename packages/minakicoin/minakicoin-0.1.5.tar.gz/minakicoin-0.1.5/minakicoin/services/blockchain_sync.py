# services/blockchain_sync.py

import httpx
import json
from minakicoin.models.block import Block
from minakicoin.services.blockchain_store_sqlite import save_chain, load_chain

async def sync_blockchain_from_peer(peer_url: str):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{peer_url}/chain/rawdb")
            if res.status_code != 200:
                print(f"❌ Failed to fetch chain from {peer_url}")
                return

            peer_chain_data = res.json().get("chain", [])
            peer_chain = [Block.from_dict(b) for b in peer_chain_data]

            local_chain = load_chain()
            if len(peer_chain) > len(local_chain):
                print(f"[🔄] Syncing blockchain from {peer_url} (length: {len(peer_chain)})")
                save_chain(peer_chain)
                print(f"[✅] Replaced local chain with {len(peer_chain)} blocks from peer.")
            else:
                print(f"[ℹ️] Local chain is up to date.")
    except Exception as e:
        print(f"❌ Sync error: {e}")
