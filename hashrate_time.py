import re
import json
import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MQTT config
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Log file path
LOG_PATH = "/home/ckpool/ckpool-solo/logs/ckpool.log"

# Regex to match lines
log_regex = re.compile(r'User (\w+):({.*})')

# Setup MQTT client
client = mqtt.Client()
if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)

# Tail log file (like `tail -F`)
def follow_log(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line.strip()

# Main loop
try:
    print(f"Watching {LOG_PATH} and publishing to MQTT...")
    for log_line in follow_log(LOG_PATH):
        match = log_regex.search(log_line)
        if match:
            user = match.group(1)
            payload = json.loads(match.group(2))
            topic = f"mining/{user}"
            client.publish(topic, json.dumps(payload))
            print(f"Published to {topic}")
except KeyboardInterrupt:
    print("Stopped.")
finally:
    client.disconnect()
