FROM python:3.9-alpine

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install influxdb_client
RUN pip install paho-mqtt python-etcd
RUN pip install requests
# RUN pip install aiocoap

RUN python ./Indus/water_inflow_sensor1_indus.py
RUN python ./Indus/water_outflow_sensor2_indus.py
# RUN python ./Indus/humidity_sensor1_indus.py
# RUN python ./Indus/humidity_sensor2_indus.py
# RUN python ./Indus/temperature_sensor1_indus.py
# RUN python ./Indus/temperature_sensor2_indus.py

RUN python ./Jehlum/water_inflow_sensor1_jehlum.py
RUN python ./Jehlum/water_outflow_sensor2_jehlum.py
# RUN python ./Jehlum/humidity_sensor1_jehlum.py
# RUN python ./Jehlum/humidity_sensor2_jehlum.py
# RUN python ./Jehlum/temperature_sensor1_jehlum.py
# RUN python ./Jehlum/temperature_sensor2_jehlum.py

# CMD ["python", "./subscriber_server/coap_server.py"]
# CMD ["python", "simulator.py"]