# source ~/bitcoin-venv/bin/activate

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json

# Save original json.loads before patching
original_json_loads = json.loads

# Patch json.loads to avoid decimal.InvalidOperation
import bitcoinrpc.authproxy
def patched_json_loads(s, *args, **kwargs):
    kwargs.pop("parse_float", None)
    return original_json_loads(s, *args, **kwargs)

bitcoinrpc.authproxy.json = json
bitcoinrpc.authproxy.json.loads = patched_json_loads

# Get credentials from environment
rpc_user = os.getenv("RPC_USER")
rpc_password = os.getenv("RPC_PASSWORD")

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:8332")

try:
    mining_info = rpc_connection.getmininginfo()
    print(f"Raw mining_info: {mining_info}")
    print(f"Difficulty: {mining_info.get('difficulty')}")
except JSONRPCException as json_exc:
    print(f"JSON RPC error: {json_exc}")
except Exception as e:
    print(f"Error: {e}")
