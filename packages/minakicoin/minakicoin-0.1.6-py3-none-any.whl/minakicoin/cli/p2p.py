import click
import uvicorn
from minakicoin.p2p_node.api import app

@click.group()
def p2p():
    """P2P Networking Commands"""
    pass

@p2p.command("start")
@click.option("--port", default=7777, help="Port to run node on")
def start_node(port):
    uvicorn.run(app, host="0.0.0.0", port=port)
