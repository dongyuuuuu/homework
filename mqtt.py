import paho.mqtt.client as paho
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
 
# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

#MQTT broker hosted on local machine
mqttc = paho.Client()
# Setting for connection
# TODO: revise host to your IP
host = "172.20.10.14"
topic = "Mbed"
# call
global data
data = {}
global ticker
ticker = 0
Fs = 10.0
Ts = 1.0/Fs
x = np.arange(0,2,Ts)
y = np.arange(0,2,Ts)
z = np.arange(0,2,Ts)
t = np.arange(0,2,Ts)

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    global data
    data = (str(msg.payload)).split()
    global ticker
    ticker = 0

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

num = 0
while num != 5:
    mqttc.loop()
    sleep(1.5)
    num += 1

for i in range(0, 20):
    mqttc.loop()
    x[i] = int(data[1])
    y[i] = int(data[2])
    z[i] = int(data[3])

while ticker != 2:
    mqttc.loop()
    ticker += 1
    sleep(0.1)

fig, ax = plt.subplots(3, 1)
ax[0].plot(t, x)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('x')
ax[1].plot(t, y)
ax[1].set_xlabel('Time')
ax[1].set_ylabel('y')
ax[2].plot(t, z)
ax[2].set_xlabel('Time')
ax[2].set_ylabel('z')
plt.show()

mqttc.loop_forever()