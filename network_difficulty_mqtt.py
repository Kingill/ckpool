# Get RPC credentials
rpc_user = os.getenv("RPC_USER")
rpc_password = os.getenv("RPC_PASSWORD")

if not rpc_user or not rpc_password:


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
