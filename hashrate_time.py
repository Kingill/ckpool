#!/usr/bin/env python3

import re
import json
import os
import time
import logging
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Load env vars
load_dotenv("/etc/hashrate/.env")

# Config
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
LOG_PATH = "/home/ckpool/ckpool-solo/logs/ckpool.log"

log_regex = re.compile(r'User (\w+):({.*})')

# Connect to MQTT
def connect_mqtt():
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

client = connect_mqtt()

# Wait for log file
while not os.path.isfile(LOG_PATH):
    logging.info(f"Waiting for log file: {LOG_PATH}")
    time.sleep(2)

def follow_log(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line.strip()

try:
    logging.info(f"Monitoring log file: {LOG_PATH}")
    for log_line in follow_log(LOG_PATH):
        match = log_regex.search(log_line)
        if match:
            user = match.group(1)
            try:
                payload = json.loads(match.group(2))
                topic = f"mining/{user}"
                client.publish(topic, json.dumps(payload))
                logging.info(f"Published to {topic}")
            except json.JSONDecodeError as e:
                logging.warning(f"Invalid JSON: {e}")
            except Exception as e:
                logging.error("MQTT publish error", exc_info=True)
except KeyboardInterrupt:
    logging.info("Stopped by user.")
finally:
    client.disconnect()
