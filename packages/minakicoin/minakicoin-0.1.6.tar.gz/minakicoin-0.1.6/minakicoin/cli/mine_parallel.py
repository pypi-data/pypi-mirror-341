# minakicoin/cli/mine_parallel.py

import click
import httpx
from minakicoin.services.mining_parallel_engine import mine_block_parallel
from minakicoin.p2p_node.state import known_peers

@click.command("mine-parallel")
@click.argument("miner")
@click.option("--threads", default=4, help="Number of threads to use")
def mine_parallel(miner, threads):
    """Mine a block using multi-threaded CPU miner."""
    click.echo(f"🚀 Starting multi-threaded mining for {miner} using {threads} threads")

    block = mine_block_parallel(miner, threads)
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
