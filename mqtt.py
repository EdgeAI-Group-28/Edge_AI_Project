import time
import json
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Replace these values with your setup
ENDPOINT = "your-endpoint.iot.<region>.amazonaws.com"
CLIENT_ID = "basicPubSub"
PATH_TO_CERT = "Jetsone.cert.pem"
PATH_TO_KEY = "Jetsone.private.key"
PATH_TO_ROOT = "root-CA.crt"
TOPIC = "Employee"

# MQTT connection setup
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6
)

print(f"Connecting to {ENDPOINT} with client ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# Publish message
message = {
    "employee_id": "E001",
    "status": "Active",
    "timestamp": time.time()
}

message_json = json.dumps(message)

print(f"Publishing message to topic '{TOPIC}': {message_json}")
mqtt_connection.publish(
    topic=TOPIC,
    payload=message_json,
    qos=mqtt.QoS.AT_LEAST_ONCE
)

time.sleep(1)

# Disconnect
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")
