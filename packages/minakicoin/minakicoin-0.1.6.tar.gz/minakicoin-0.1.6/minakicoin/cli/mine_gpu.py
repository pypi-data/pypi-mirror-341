# minakicoin/cli/mine_gpu.py

import click
import httpx
from minakicoin.services.mining_gpu_engine import mine_block_gpu
from minakicoin.p2p_node.state import known_peers

@click.command("mine-gpu")
@click.argument("miner")
def mine_gpu(miner):
    """Mine a block using GPU (CUDA)"""
    click.echo(f"🚀 Starting GPU mining for {miner}")

    block = mine_block_gpu(miner)
    if not block:
        click.secho("❌ Failed to mine block", fg="red")
        return

    click.secho(f"✅ Mined block #{block.index}: {block.hash}", fg="green")

    for peer in known_peers:
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{peer}/broadcast/block",
                    json={"block": block.to_dict()},
                    timeout=3
                )
                if response.status_code == 200:
                    click.echo(f"📡 Sent block to {peer}")
                else:
                    click.secho(f"⚠️ Peer {peer} responded with {response.status_code}", fg="yellow")
        except Exception as e:
            click.secho(f"⚠️ Failed to broadcast to {peer}: {e}", fg="yellow")
