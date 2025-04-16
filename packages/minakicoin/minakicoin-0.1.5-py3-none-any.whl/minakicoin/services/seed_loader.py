import json
import os

SEED_FILE = os.path.join(os.path.dirname(__file__), '../../seeds.json')

def get_seeds():
    try:
        with open(SEED_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []
