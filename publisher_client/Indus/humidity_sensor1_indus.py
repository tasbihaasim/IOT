'''For the humidity of city of Sheikhupura'''
# client_put.py
import asyncio
import random
import requests

#import pandas as pd

from aiocoap import *
import aiocoap.resource as resource
import aiocoap

# url = 'http://www.wapda.gov.pk/index.php/river-flow-data'
# link = "http://www.wapda.gov.pk/index.php/river-flow-data"
# dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)

import datetime
import os

coap_server_uri = os.environ.get('COAP_SERVER_URI', 'coap://127.0.0.1:5683/Indus_humidity_sensor1')




async def main():
    context = await Context.create_client_context()
    today = datetime.datetime.now()
    month = today.strftime("%b")
    temp = 0
    if month == 'Nov' or month == 'Dec' or month == 'Jan' or month == 'Feb':
        temp = random.randint(27, 33)
    if month == 'March' or month == 'April' or month == 'May':
        temp = random.randint(18, 24)
    if month == 'June' or month == 'July' or month == 'August':
        temp = random.randint(37, 60)
    if month == 'Sep' or month == 'Oct' or month == 'Nov':
        temp = random.randint(28, 50)

    for i in range(24):
        rn = random.randint(1,4)
        c = random.choice(["increment", "decrement"])
        if c=="increment":
            temp = temp + rn
        else:
            temp = temp - rn
        data = "{}".format(temp)

        request = Message(code=POST, payload=data.encode("ascii"), uri='coap://127.0.0.1:5683/Indus_humidity_sensor1')
        try:
            response = await context.request(request).response
        except Exception as e:
            print('Failed to send data:')
            print(e)
        else:
            print('Sent data:', data)
            print('Received ACK:', response.payload.decode("ascii"))
        #await asyncio.sleep(2)

asyncio.get_event_loop().run_until_complete(main())

