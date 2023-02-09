'''For the temperature of city of Qambar'''
# client_put.py
import asyncio
import random
import requests

# import pandas as pd

from aiocoap import *
import datetime
# url = 'http://www.wapda.gov.pk/index.php/river-flow-data'
# link = "http://www.wapda.gov.pk/index.php/river-flow-data"
# dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)
#
# Indus_date = dfs[0][0]

async def main():
    context = await Context.create_client_context()
    today = datetime.datetime.now()
    month = today.strftime("%b")
    temp = 0

    if month == 'Nov' or month == 'Dec' or month == 'Jan' or month == 'Feb':
        temp = random.randint(12, 24)
    if month == 'March' or month == 'April' or month == 'May':
        temp = random.randint(21, 45)
    if month == 'June' or month == 'July' or month == 'August':
        temp = random.randint(33, 44)
    if month == 'Sep' or month == 'Oct' or month == 'Nov':
        temp = random.randint(26, 38)

    for i in range(24):
        rn = random.randint(1, 4)
        c = random.choice(["increment", "decrement"])
        if c == "increment":
            temp = temp + rn
        else:
            temp = temp - rn
        data = "{}".format(temp)
        request = Message(code=POST, payload=data.encode("ascii"), uri='coap://127.0.0.1:5683/Indus_temperature_sensor2')
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




