import csv
import re

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

token = 'skVO0ckLCISprVeTI43CrtXCk1NSoJmlGQlN_X1FfpzOJ48c5JTatF4Tb3p-sRYtkaJ52vjFKCqcI5wrrpqGAg=='
org = "robelamare20@gmail.com"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Prepare the data
measurements = ['inflow', 'outflow', 'humidity', 'temperature', 'level']
data = [
    {
        "measurement": measurements[0],
        "tags": {
            "host": "server01"
        },
        "fields": {
            "value": 25
        }
    },
    {
        "measurement": measurements[1],
        "tags": {
            "host": "server01"
        },
        "fields": {
            "value": 100
        }
    },
{
        "measurement": measurements[2],
        "tags": {
            "host": "server01"
        },
        "fields": {
            "value": 100
        }
    },
{
        "measurement": measurements[3],
        "tags": {
            "host": "server01"
        },
        "fields": {
            "value": 100
        }
    },
{
        "measurement": measurements[4],
        "tags": {
            "host": "server01"
        },
        "fields": {
            "value": 100
        }
    },
]

bucket1 = 'indus'
bucket2 = 'jehlum'
write_api = client.write_api(write_options=SYNCHRONOUS)

with open('rawdata.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)

    # Iterate over the rows of the CSV file
    for row in reader:
        t = tuple(row)
        row = re.split(r'[\/_]', t[0]) ## [ list of three items ]

        '''FOR INDUS'''
        if row[0] == "Indus":
            city1 = 'Sheikhupura'
            if row[2] == 'sensor2':
                city1 = 'Qambar'
            point1 = (
                Point(row[1])
                .tag("location", city1)
                .field("value", int(t[1]))
            )
            # print(point)
            write_api.write(bucket=bucket1, org="robelamare20@gmail.com", record=point1)
        '''FOR JEHLUM'''
        if row[0] == "Jehlum":
            print(2)
            city2 = 'Srinagar'
            if row[2] == 'sensor2':
                city2 = 'Muzaffarabad'
            point2 = (
                Point(row[1])
                .tag("location", city2)
                .field("value", int(t[1]))
            )
            # print(point)
            write_api.write(bucket=bucket2, org="robelamare20@gmail.com", record=point2)


        # t = tuple(row)
        # arr = re.split(r'[\/_]', t[0])
        # print(arr, t[1])