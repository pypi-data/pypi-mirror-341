# minakicoin/p2p_node/services/sync.py

from minakicoin.services.blockchain_store_sqlite import save_chain
from minakicoin.services.blockchain import get_blockchain
from minakicoin.services.utxo_store_sqlite import add_utxos, spend_utxos
from minakicoin.models.block import Block
from minakicoin.models.transactions import TxOutput
from minakicoin.p2p_node.state import known_peers
from minakicoin.config import config

import httpx
import sqlite3


def calculate_block_work(hash: str) -> int:
    """Work = 2^n where n = number of leading zeros"""
    n = 0
    for c in hash:
        if c == "0":
            n += 1
        else:
            break
    return 2 ** n


def calculate_total_work(headers: list[dict]) -> int:
    return sum(calculate_block_work(h["hash"]) for h in headers if "hash" in h)


async def sync_chain_from_peers():
    print("[🌍] Attempting to sync chain from peers...")

    local_chain = get_blockchain()
    local_work = sum(calculate_block_work(b.hash) for b in local_chain)

    for peer in known_peers:
        try:
            async with httpx.AsyncClient() as client:
                # 🔗 Step 1: Pull headers
                res = await client.get(f"{peer}/headers")
                if res.status_code != 200:
                    print(f"[⚠️] {peer}/headers returned {res.status_code}")
                    continue

                headers = res.json()
                remote_work = calculate_total_work(headers)

                if remote_work > local_work:
                    print(f"[🔄] Remote chain from {peer} has more work — syncing blocks...")

                    # 📦 Step 2: Get full chain
                    block_res = await client.get(f"{peer}/chain")
                    if block_res.status_code != 200:
                        print(f"[❌] Failed to fetch chain from {peer}")
                        continue

                    json_data = block_res.json()
                    if isinstance(json_data, dict) and "chain" in json_data:
                        remote_chain_raw = json_data["chain"]
                    else:
                        remote_chain_raw = json_data

                    remote_chain = [Block.from_dict(b) for b in remote_chain_raw]

                    save_chain(remote_chain)

                    # 💾 Step 3: Rebuild UTXO set
                    conn = sqlite3.connect(config.UTXO_DB)
                    conn.execute("DELETE FROM utxos")
                    conn.commit()
                    conn.close()

                    for block in remote_chain:
                        for tx in block.transactions:
                            if tx.sender != "COINBASE":
                                spend_utxos(tx.inputs)

                            outputs = [TxOutput.from_dict(o) if isinstance(o, dict) else o for o in tx.outputs]
                            add_utxos(tx.txid, outputs)

                    print(f"[✅] Chain + UTXOs synced from {peer}")
                else:
                    print(f"[🟰] Local chain has more or equal work than {peer}")
        except Exception as e:
            print(f"[⚠️] Failed to sync from {peer}: {e}")
