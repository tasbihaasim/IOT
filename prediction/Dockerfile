FROM python:3.8-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install influxdb_client
#RUN pip install paho-mqtt python-etcd
#RUN pip install requests
#RUN pip install aiocoap
RUN pip install twilio
RUN pip install -U scikit-learn
RUN pip install pandas
RUN pip install numpy==1.23.5

RUN python predictor.py config.json
# CMD ["python", "./subscriber_server/coap_server.py"]
#CMD ["python", "simulator.py"]