import paho.mqtt.client as mqtt
import json

samples = []

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180da/arduino/nnhien")

def on_message(client, userdata, message):
    #print(str(time.time()) + ': Received message: "' + str(message.payload) + '" on topic "' +
    #    message.topic + '" with QoS ' + str(message.qos))
    data = message.payload.decode()
    samples.append(json.loads(data))
    if len(samples) > 20:
        samples.pop(0)
        forward = all(sample["ax"] > 0.2 for sample in samples[-5:])
        up = all(sample["az"] < 0.7 for sample in samples[-5:])
        circle = sum(sample["gx"] * 0.075 for sample in samples) > 360 or sum(sample["gx"] * 0.075 for sample in samples) < -360
        idle = all(sample["ax"] < 0.1 and sample["ay"] < 0.4 and sample["az"] > 0.9 and sample["az"] < 1.1 for sample in samples)

        if forward:
            print("forward")
        if up:
            print("up")
        if circle:
            print("circle")
        if idle:
            print("idle")
        

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com")
client.loop_forever()