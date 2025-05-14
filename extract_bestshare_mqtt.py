import re
import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Config
log_path = os.getenv("CKPOOL_LOG", "/home/ckpool/ckpool-solo/logs/ckpool.log")
mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
mqtt_port = int(os.getenv("MQTT_PORT", 1883))
mqtt_topic = os.getenv("MQTT_TOPIC", "ckpool/bestshare")
mqtt_username = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Regex to find bestshare
bestshare_pattern = r'bestshare":\s*(\d+)'

def extract_latest_bestshare(log_file):
    bestshare = None
    try:
        with open(log_file, "r") as f:
            for line in reversed(f.readlines()):
                match = re.search(bestshare_pattern, line)
                if match:
                    bestshare = int(match.group(1))
                    break
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
    except Exception as e:
        print(f"Error reading log file: {e}")
    return bestshare

if __name__ == "__main__":
    bestshare = extract_latest_bestshare(log_path)

    if bestshare is not None:
        print(f"Latest bestshare: {bestshare}")

        # Send via MQTT in JSON
        payload = json.dumps({"bestshare": bestshare})
        try:
            client = mqtt.Client(protocol=mqtt.MQTTv5)
            if mqtt_username and mqtt_password:
                client.username_pw_set(mqtt_username, mqtt_password)

            client.connect(mqtt_broker, mqtt_port, 60)
            client.publish(mqtt_topic, payload)
            client.disconnect()
            print(f"✅ Published to MQTT topic '{mqtt_topic}': {payload}")
        except Exception as e:
            print(f"❌ MQTT publish error: {e}")
    else:
        print("No bestshare found in log.")
