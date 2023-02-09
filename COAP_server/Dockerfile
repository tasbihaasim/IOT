FROM python:3.9-alpine

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install influxdb_client
RUN pip install paho-mqtt python-etcd
RUN pip install requests
RUN pip install aiocoap

#RUN python coap_server.py
CMD ["python", "coap_server.py"]
#CMD ["python", "./publisher_client/Indus/humidity_sensor1_indus"]