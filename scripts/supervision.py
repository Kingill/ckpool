import requests
import json
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    #handlers=[logging.StreamHandler(), logging.FileHandler('server_monitor.log')]
    handlers=[logging.StreamHandler(), logging.FileHandler('/home/ckpool/logs/server_monitor.log')]

)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate environment variables
required_env_vars = ["MQTT_BROKER", "MQTT_PORT", "MQTT_USER", "MQTT_PASSWORD"]
for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Missing environment variable: {var}")
        exit(1)

# Configuration
servers = [
    { "name": "bitaxe", "url": "http://192.168.1.19" },
    { "name": "bitaxe2", "url": "http://192.168.1.51" }
]

timeout = int(os.getenv("HTTP_TIMEOUT", 5))  # Default to 5 seconds
MQTT_BROKER = os.getenv("MQTT_BROKER")
try:
    MQTT_PORT = int(os.getenv("MQTT_PORT"))
except ValueError:
    logger.error("MQTT_PORT must be a valid integer")
    exit(1)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "supervision/bitaxe")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code: {rc}")

def on_publish(client, userdata, mid):
    logger.info(f"Message {mid} published successfully")

# Check server status
def check_servers():
    results = []
    for server in servers:
        name = server["name"]
        url = server["url"]
        try:
            response = requests.get(url, timeout=timeout)
            status = 1 if response.status_code == 200 else 0
            results.append({name: status})
            logger.info(f"Checked {name} ({url}): {'OK' if status else 'DOWN'}")
        except requests.RequestException as e:
            results.append({name: 0})
            logger.warning(f"Failed to reach {name} ({url}): {str(e)}")
    return results


# Main function
def main():
    # Set up MQTT client
    #client = mqtt.Client()
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_publish = on_publish
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    # Connect to MQTT broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {str(e)}")
        return

    # Check servers and publish results
    payload = json.dumps(check_servers())
    try:
        client.publish(MQTT_TOPIC, payload, qos=1)
        logger.info(f"Published to {MQTT_TOPIC}: {payload}")
    except Exception as e:
        logger.error(f"Failed to publish to MQTT: {str(e)}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
