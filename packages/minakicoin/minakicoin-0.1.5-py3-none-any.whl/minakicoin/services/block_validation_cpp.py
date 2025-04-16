# minakicoin/services/block_validation_cpp.py

import hashlib
import json
from minakicoin.models.block import Block

BLOCK_REWARD = 50.0  # Max allowed coinbase payout

def validate_block_cpp(block: Block) -> bool:
    """
    Validate a block mined via the C++ miner using a simplified hash:
    - Only index, previous_hash, timestamp, nonce, tx_summary are used
    - Skips full transaction validation
    - Accepts block if simplified hash matches and PoW is met
    """
    print(f"🔍 [C++] Validating block: {block.hash[:10]}...")

    # 1. Reconstruct the simplified dict used for C++ hashing
    if not hasattr(block, "tx_summary"):
        # Try to reconstruct summary from transactions
        try:
            txids = [tx.txid for tx in block.transactions]
            summary = "+".join(txids)
        except Exception as e:
            print(f"❌ Can't compute tx_summary: {e}")
            return False
    else:
        summary = block.tx_summary

    simplified = {
        "index": block.index,
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "nonce": block.nonce,
        "tx_summary": summary
    }

    recalculated = hashlib.sha256(json.dumps(simplified, sort_keys=True).encode()).hexdigest()

    if block.hash != recalculated:
        print(f"⚠️ Hash mismatch (C++): block = {block.hash}, recalculated = {recalculated}")
        return False

    # 2. Proof of Work check
    if not block.hash.startswith("00"):  # Or adjust difficulty here
        print(f"⚠️ Block does not meet difficulty target: {block.hash}")
        return False

    print("✅ [C++] Block passed simplified validation")
    return True
