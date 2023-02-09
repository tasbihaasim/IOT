'''For the temperature of city of Srinagar'''
# client_put.py
import asyncio
import random
import requests

# import pandas as pd

from aiocoap import *

# url = 'http://www.wapda.gov.pk/index.php/river-flow-data'
# link = "http://www.wapda.gov.pk/index.php/river-flow-data"
# dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)

# Indus_date = dfs[0][0]
import datetime


async def main():
    context = await Context.create_client_context()
    today = datetime.datetime.now()
    month = today.strftime("%b")
    temp = 0
    if month == 'Nov' or month == 'Dec' or month == 'Jan' or month == 'Feb':
        temp = random.randint(-2, 16)
    if month == 'March' or month == 'April' or month == 'May':
        temp = random.randint(0, 21)
    if month == 'June' or month == 'July' or month == 'August':
        temp = random.randint(11, 30)
    if month == 'Sep' or month == 'Oct' or month == 'Nov':
        temp = random.randint(6, 28)
    for i in range(24):
        rn = random.randint(1, 4)
        c = random.choice(["increment", "decrement"])
        if c == "increment":
            temp = temp + rn
        else:
            temp = temp - rn
        data = "{}".format(temp)
        request = Message(code=POST, payload=data.encode("ascii"), uri='coap://127.0.0.1:5683/Jehlum_temperature_sensor1')
        try:
            response = await context.request(request).response
            # print(response)
        except Exception as e:
            print('Failed to send data:')
            print(e)
        else:
            print('Sent data:', data)
            print('Received ACK:', response.payload.decode("ascii"))
        #await asyncio.sleep(2)

asyncio.get_event_loop().run_until_complete(main())
