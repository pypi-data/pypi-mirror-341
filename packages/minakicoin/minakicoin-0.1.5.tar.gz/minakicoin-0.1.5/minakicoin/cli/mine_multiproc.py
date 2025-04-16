# minakicoin/cli/mine_multiproc.py

import click
import httpx
import multiprocessing
from minakicoin.services.mining_multiproc_engine import mine_block_multiproc
from minakicoin.p2p_node.state import known_peers

@click.command("mine-multiproc")
@click.argument("miner")
# @click.option("--processes", default=None, help="Number of processes to use (default: max available cores)")
@click.option("--processes", default=None, type=int, help="Number of processes to use (default: max available cores)")
def mine_multiproc(miner, processes):
    """Mine a block using multiprocessing (true multi-core)."""
    
    # Auto-detect CPU core count if not provided
    if processes is None:
        processes = multiprocessing.cpu_count()

    click.echo(f"🚀 Starting multi-process mining for {miner} using {processes} processes")

    block = mine_block_multiproc(miner, processes)
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
