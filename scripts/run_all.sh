#!/bin/bash
source /home/ckpool/bitcoin-venv/bin/activate

python3 /home/ckpool/scripts/bitaxe_api_to_mqtt.py
python3 /home/ckpool/scripts/bitaxe2_api_to_mqtt.py
python3 /home/ckpool/scripts/network_difficulty_mqtt.py
