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
client.loop_start()  # assure la reconnexion automatique

# Tail log file
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
    last_heartbeat = time.time()

    for log_line in follow_log(LOG_PATH):
        now = time.time()
        if now - last_heartbeat > 300:  # 5 minutes
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Still alive, waiting for log...")
            last_heartbeat = now

        match = log_regex.search(log_line)
        if match:
            user = match.group(1)
            try:
                payload = json.loads(match.group(2))
                topic = f"mining/{user}"
                client.publish(topic, json.dumps(payload))
                print(f"Published to {topic}")
            except json.JSONDecodeError as e:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] JSON decode error: {e}")
                print(f"Line causing issue: {match.group(2)}")
            except Exception as e:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unexpected error: {e}")

except KeyboardInterrupt:
    print("Stopped.")
finally:
    client.loop_stop()
    client.disconnect()
