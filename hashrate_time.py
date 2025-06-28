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
    file = open(file_path, 'r')
    file.seek(0, os.SEEK_END)
    inode = os.fstat(file.fileno()).st_ino

    while True:
        line = file.readline()
        if line:
            yield line.strip()
        else:
            try:
                # Check if file was rotated
                if os.stat(file_path).st_ino != inode:
                    new_file = open(file_path, 'r')
                    file.close()
                    file = new_file
                    inode = os.fstat(file.fileno()).st_ino
                    print("Log file rotated — reopened.")
                time.sleep(0.2)
            except FileNotFoundError:
                time.sleep(0.5)



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
