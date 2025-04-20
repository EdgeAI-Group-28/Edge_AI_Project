import os
import time
import json
import datetime
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from flask import Flask, request, jsonify


app = Flask(__name__)

ENDPOINT = "a4e2wanb9d9uz-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "basicPubSub"
PATH_TO_CERT = "Credentials/Jetson.cert.pem"
PATH_TO_KEY = "Credentials/Jetson.private.key"
PATH_TO_ROOT = "Credentials/root-CA.crt"
TOPIC = "RDS"


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



def SendDataToMQTT(data, table):

    global mqtt_connection

    message = {
        "timestamp": datetime.now(),
        "device_id": "JetsonNano",
        "data": data,
        "task":"insert",
        "table": table
    }

    message_json = json.dumps(message)
    print("*** Message to be published:", message_json)

    print(f"Publishing message to topic ': {message_json}")
    publish_future, _ = mqtt_connection.publish(
        topic=TOPIC,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    publish_future.result() 
    print("Message published.")




def disconnect():
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")



@app.route('/', methods=['GET'])
def startFlask():
    return jsonify({"status": "success"}), 200


@app.route('/', methods=['POST'])
def receive_data():

    content = request.get_json()
    data = content.get("data")
    table = content.get("table")


    if data == "exit":
        disconnect()
    
    SendDataToMQTT(data, table)

    print("Received in Docker:", data)
    return jsonify({"status": "success", "received": data}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    
