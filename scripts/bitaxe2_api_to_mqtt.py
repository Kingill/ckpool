import requests
import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load .env config
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://192.168.1.51/api/system/info")
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "bitaxe2/status")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

def fetch_api_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return None

def publish_to_mqtt(payload):
    try:
        client = mqtt.Client()
        if MQTT_USER and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(MQTT_TOPIC, json.dumps(payload))
        client.disconnect()
        print(f"✅ Published to MQTT topic '{MQTT_TOPIC}': {json.dumps(payload)}")
    except Exception as e:
        print(f"❌ MQTT publish error: {e}")

if __name__ == "__main__":
    data = fetch_api_data(API_URL)
    if data:
        # You can modify this to include whatever fields you care about
        filtered = {
            "hostname": data.get("hostname"),
            "hashRate": data.get("hashRate"),
            "power": data.get("power"),
            "voltage": data.get("voltage"),
            "temp": data.get("temp"),
            "sharesAccepted": data.get("sharesAccepted"),
            "sharesRejected": data.get("sharesRejected"),
            "uptimeSeconds": data.get("uptimeSeconds"),
            "wifiRSSI": data.get("wifiRSSI")
        }
        publish_to_mqtt(filtered)
