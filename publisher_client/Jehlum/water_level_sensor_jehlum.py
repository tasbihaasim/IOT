import requests
# import pandas as pd
import paho.mqtt.client as mqtt #import the client1
import random
import time

from paho.mqtt import client as mqtt_client


# link = "http://www.wapda.gov.pk/index.php/river-flow-data"
# dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)
# Indus_inflow = dfs[0][5]

# columns = ['Date', 'Indus at Tarbela Level (ft)', 'Indus at Tarbela Inflow (cfs)',
#            'Indus at Tarbela Outflow (cfs)', 'Kabul at Nowshera Inflow (cfs)',
#            'Jhelum at Mangla Level (ft)', 'Jhelum at Mangla Inflow (cfs)',
#            'Jhelum at Mangla Outflow (cfs)', 'Chenab at Marala Inflow (cfs)',
#            'Total Inflow Current Year (cfs)', 'Total Inflow Last Year (cfs)',
#            'Total Inflow Average Last 10 Years (cfs)']

broker = 'broker.emqx.io'
# broker = 'localhost'
port = 1883
topic = "Jehlum/level/sensor1"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

flood_chance = 0.2
def publish(client):
    msg_count = 0
    for i in range(25):
        #time.sleep(1)
        msg = f"messages: {msg_count}"
        val = i
        if random.uniform(0, 1) <= flood_chance:
            val = i + 100
        result = client.publish(topic, val)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

# broker_address="localhost"
# client = mqtt.Client("P1")
# client.connect(broker_address) #connect to broker
# client.loop_start()
#
# def publish():
#     for i in Indus_inflow:
#         client.publish("Indus/inflow/sensor1", i)
#         break
# client.loop_stop()
