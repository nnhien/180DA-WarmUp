import paho.mqtt.client as mqtt
import time
import sys

pub = int(sys.argv[1])
recv = int(sys.argv[2])

PUB_TOPIC = f'180da/nnhien/{pub}'
RECV_TOPIC = f'180da/nnhien/{recv}'

def on_connect(client, userdata, flags, rc):
    print("Connected!")

    print(f'subscribing to {RECV_TOPIC}')
    client.subscribe(RECV_TOPIC, qos=1)

    print(f'publishing 0 to {RECV_TOPIC}')
    client.publish(PUB_TOPIC, int(0), qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    payload = int(message.payload)
    print(f'Received payload: {payload} from {RECV_TOPIC}')
    time.sleep(1)
    print(f'Sending payload: {payload + 1} to {PUB_TOPIC}')
    client.publish(PUB_TOPIC, payload + 1, qos=1)

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever(timeout=5)