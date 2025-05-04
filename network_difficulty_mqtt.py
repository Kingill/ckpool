import os
import json
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import bitcoinrpc.authproxy
import paho.mqtt.client as mqtt

# Load environment variables
load_dotenv()

# Patch json.loads to avoid decimal.InvalidOperation
original_json_loads = json.loads
def patched_json_loads(s, *args, **kwargs):
    kwargs.pop("parse_float", None)
    return original_json_loads(s, *args, **kwargs)

bitcoinrpc.authproxy.json = json
bitcoinrpc.authproxy.json.loads = patched_json_loads

# Get RPC credentials
rpc_user = os.getenv("RPC_USER")
rpc_password = os.getenv("RPC_PASSWORD")

if not rpc_user or not rpc_password:
    raise ValueError("Missing RPC_USER or RPC_PASSWORD in environment.")

# MQTT settings
mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
mqtt_port = int(os.getenv("MQTT_PORT", 1883))
mqtt_topic = os.getenv("MQTT_TOPIC", "bitcoin/mininginfo")

# Connect to Bitcoin RPC
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:8332")

try:
    mining_info = rpc_connection.getmininginfo()

    # Optional: format hashrate to EH/s (float)
    mining_info["networkhashps_EHs"] = mining_info["networkhashps"] / 1e18

    # Serialize to JSON
    json_payload = json.dumps(mining_info)

    # Publish to MQTT
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(mqtt_topic, json_payload)
    client.disconnect()

    print(f"✅ Published mining info to MQTT topic '{mqtt_topic}':\n{json_payload}")

except JSONRPCException as json_exc:
    print(f"JSON RPC error: {json_exc}")
except Exception as e:
    print(f"Error: {e}")
