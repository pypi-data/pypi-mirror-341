# minakicoin/p2p_node/routes/status.py

from fastapi import APIRouter
from minakicoin.services.mempool import load_mempool
from minakicoin.services.blockchain import get_blockchain
from minakicoin.p2p_node.state import known_peers

router = APIRouter()

@router.get("/status")
def status():
    chain = get_blockchain()
    mempool = load_mempool(raw=True)
    return {
        "height": len(chain) - 1,
        "latest_block_hash": chain[-1].hash if chain else None,
        "mempool_tx_count": len(mempool),
        "known_peers": len(known_peers)
    }
