import os
import json
import logging
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import bitcoinrpc.authproxy
import paho.mqtt.client as mqtt
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Patch json.loads to avoid decimal.InvalidOperation
original_json_loads = json.loads
def patched_json_loads(s, *args, **kwargs):
    kwargs.pop("parse_float", None)
    return original_json_loads(s, *args, **kwargs)

# Temporarily patch json.loads for RPC calls
@contextmanager
def patched_json():
    bitcoinrpc.authproxy.json = json
    bitcoinrpc.authproxy.json.loads = patched_json_loads
    try:
        yield
    finally:
        bitcoinrpc.authproxy.json.loads = original_json_loads

# Get environment variables
rpc_user = os.getenv("RPC_USER")
rpc_password = os.getenv("RPC_PASSWORD")
rpc_host = os.getenv("RPC_HOST", "127.0.0.1")
rpc_port = os.getenv("RPC_PORT", "8332")
mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
mqtt_port = os.getenv("MQTT_PORT", "1883")
mqtt_topic = os.getenv("MQTT_TOPIC", "bitcoin/mininginfo")
mqtt_user = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Validate environment variables
required_vars = {"RPC_USER": rpc_user, "RPC_PASSWORD": rpc_password}
for var_name, var_value in required_vars.items():
    if not var_value:
        logger.error(f"Missing required environment variable: {var_name}")
        raise ValueError(f"Missing {var_name} in environment.")

try:
    mqtt_port = int(mqtt_port)
except ValueError:
    logger.error(f"Invalid MQTT_PORT: {mqtt_port}")
    raise ValueError("MQTT_PORT must be a valid integer.")

# Connect to Bitcoin RPC
rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
rpc_connection = AuthServiceProxy(rpc_url)

# MQTT client setup
mqtt_client = mqtt.Client()

# Set MQTT username and password if provided
if mqtt_user and mqtt_password:
    mqtt_client.username_pw_set(mqtt_user, mqtt_password)
    logger.debug("MQTT authentication set with provided username and password")
elif mqtt_user or mqtt_password:
    logger.warning("Both MQTT_USER and MQTT_PASSWORD must be set for authentication. Skipping auth.")

try:
    with patched_json():
        # Get mining info
        mining_info = rpc_connection.getmininginfo()
        mining_info["networkhashps_EHs"] = mining_info["networkhashps"] / 1e18

    # Serialize to JSON
    json_payload = json.dumps(mining_info)

    # Connect to MQTT broker
    mqtt_client.connect(mqtt_broker, mqtt_port, keepalive=60)
    mqtt_client.publish(mqtt_topic, json_payload)
    logger.info(f"Published mining info to MQTT topic '{mqtt_topic}': {json_payload}")

except JSONRPCException as json_exc:
    logger.error(f"JSON RPC error: {json_exc}")
except ConnectionRefusedError as conn_err:
    logger.error(f"MQTT connection failed: {conn_err}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    # Ensure MQTT client disconnects
    try:
        mqtt_client.disconnect()
        logger.debug("Disconnected from MQTT broker")
    except Exception as e:
        logger.warning(f"Failed to disconnect MQTT client: {e}")
