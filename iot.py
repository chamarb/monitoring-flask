import paho.mqtt.client as mqtt
import random
import time

MQTT_BROKER_URL = 'test.mosquitto.org'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = 'iot/humidite'

def on_connect(client, userData, flags, rc):
    if rc == 0:
        print('Connected')
    else:
        print('Disconnected')

client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)
    client.loop_start()

    while True:
        humidity = round(random.uniform(30, 100), 2)
        client.publish(MQTT_TOPIC, f'humidity: {humidity}')
        print('humidity', humidity)
        time.sleep(5)

except KeyboardInterrupt:
    print('Interrupted by user')

except Exception as e:
    print('Error:', e)

finally:
    client.disconnect()