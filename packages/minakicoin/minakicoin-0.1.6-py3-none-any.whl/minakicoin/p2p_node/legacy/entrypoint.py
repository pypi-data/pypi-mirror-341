# minakicoin/p2p_node/entrypoint.py

from minakicoin.p2p_node.api import app

# This file exists just to expose the FastAPI `app` object
# so you can run it with `uvicorn minakicoin.p2p_node.entrypoint:app --reload --port 7777`
