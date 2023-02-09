import paho.mqtt.client as mqtt #import the client1
import time
con = False
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import random
from paho.mqtt import client as mqtt_client
import csv

# token_="GtEeLWZqA42o88CVxUQg2dvBqTduZuC-NXgBVMwqZX7pce1bWhmQzMEO8woGOpPdh1wWqWZBo4Jz0U-JhpxHnQ=="
# org_="anelyamend@gmail.com"
# url_="https://us-east-1-1.aws.cloud2.influxdata.com"

token_ = '9IFfacI50A4UWiarJhnycnAyAZ5dHrCzqEvsYqCRuXT1kqstVkJ-n_drPk5qkKF1Ojiz_vVhE_ApHfJ-PrmIGQ=='
org_ = "robelamare20@gmail.com"
url_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"


client = influxdb_client.InfluxDBClient(url=url_, token=token_, org=org_)

measurements = ['inflow', 'outflow', 'level']
data = [
    {
"measurement": measurements[0],"tags": {"host": "server01"},"fields": {"value": 100}},
{
"measurement": measurements[1],"tags": {"host": "server01"},"fields": {"value": 100}},
{
"measurement": measurements[2],"tags": {"host": "server01"},"fields": {"value": 100}},
]
bucket1 = 'indus'
bucket2 = 'jehlum'
write_api = client.write_api(write_options=SYNCHRONOUS)

# f = open('C:/Users/Tasbiha/Iot/rawdata.csv', 'a', newline='')
# writer = csv.writer(f)

broker = 'broker.emqx.io'
#broker="localhost"
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            con = True
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #Data.append((msg.payload.decode(), msg.topic))
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        m = msg.topic
        arr = m.split("/")
        sen_name = arr[1]+"_"+arr[2]
        point = (
            Point(arr[1])
            .tag("sensor name", sen_name)
            .field("value", float(msg.payload.decode()))
        )

        # point = (
        #     Point(arr[0])
        #     .tag("location", arr[2])
        #     .field(arr[1], )
        # )
        # print(point)
        '''FOR INDUS'''
        if arr[0] == "Indus":
            write_api.write(bucket=bucket1, org=org_, record=point)
        '''FOR JEHLUM'''
        if arr[0] == "Jehlum":
            write_api.write(bucket=bucket2, org=org_, record=point)
        # writer.writerow((msg.topi, msg.payload.decode()))
        # print(Data)

    client.subscribe("Indus/inflow/sensor1")
    client.subscribe("Indus/outflow/sensor1")
    client.subscribe("Indus/level/sensor1")
    client.subscribe("Jehlum/inflow/sensor1")
    client.subscribe("Jehlum/outflow/sensor1")
    client.subscribe("Jehlum/level/sensor1")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

