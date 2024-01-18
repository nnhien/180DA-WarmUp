import paho.mqtt.client as mqtt
import time

self_topic = f'ece180d/nn'
next_topic = f'ece180d/ks'

def on_connect(client, userdata, flags, rc):
    print("Connected!")

    print(f'subscribing to {self_topic}')
    client.subscribe(self_topic, qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    payload = int(message.payload)
    print(f'Received payload: {payload} from {self_topic}')
    time.sleep(1)
    print(f'Sending payload: {payload + 1} to {next_topic}')
    client.publish(next_topic, payload + 1, qos=1)

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever(timeout=5)