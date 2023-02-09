#imports
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pickle
import pandas
from twilio.rest import Client
import sys
import json

token = '9IFfacI50A4UWiarJhnycnAyAZ5dHrCzqEvsYqCRuXT1kqstVkJ-n_drPk5qkKF1Ojiz_vVhE_ApHfJ-PrmIGQ=='
org = "robelamare20@gmail.com"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


#query the data
def query_db(bucket):
    query_api = client.query_api()
    if bucket == 'indus':
        query = """from(bucket: "indus")
          |> range(start: -1h)

          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          """
    if bucket == 'jehlum':
        query = """from(bucket: "jehlum")
          |> range(start: -1h)

          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          """
    data_frame_fromDB = query_api.query_data_frame_stream(query=query,org=org)
    query_result_df = []
    for df in data_frame_fromDB:
        query_result_df.append(df)
    if len(query_result_df) == 0:
        return pandas.DataFrame(query_result_df)
    if len(query_result_df) != 1:
        return query_result_df[1]
    return query_result_df[0]

#preprocess the data from the DB

def preprocess_data(dft):
    
    all_sensors = ['humidity_sensor1','humidity_sensor2','temperature_sensor1',
                   'temperature_sensor2','outflow_sensor1','inflow_sensor1']
    #get the month
    df_month = dft['_time'].dt.month
    
    list_dfs = [df_month]
    column_names_list = dft.columns.tolist()
    sensor_name = column_names_list[6]
    
    grouped = dft.groupby(sensor_name)
    
    
    # Iterate over groups and access group data
   
    total_df = [df_month]
    for name, group in grouped:
        dataf = group.reset_index(drop=True,inplace=False)
        dataf = dataf.rename(columns={'value': dataf[sensor_name][0]}, inplace=False)
        dataf = dataf.iloc[:,-1:]
        total_df.append(dataf)
    new_df = pandas.concat(total_df,axis=1)
    new_df = new_df.dropna()
    
    return new_df 

#make a prediction

def make_a_prediction(new_df,model):
    X = new_df.to_numpy()
    predictions_list = []
    rows = X.shape[0]
    print('rows')
    print(rows)
    with open(model, 'rb') as f:
        loaded_model = pickle.load(f)
    
    for i in range(rows):
        predictions_list.append(loaded_model.predict(X[i].reshape((1,7))))
        
        
    return predictions_list
    

#write to database

def write_prediction(predicted_list,bucket,threshold):
    write_api = client.write_api(write_options=SYNCHRONOUS)
   
    items = ['flood_predictions']
    for item in items:
        for value in range(len(predicted_list)):
            print('----')
            print(str(predicted_list[value] > threshold))
            print('----')
            point = (
                Point(item)
                .tag("predicted-output",int(value > threshold))
                .tag("river-name",bucket)
                .field("water-level",predicted_list[value])
            )
            write_api.write(bucket=bucket, org="robelamare20@gmail.com", record=point)

def send_sms(predicted_list,threshold,bucket,sender,receiver):
    
    
    check_Flood = False
    if any(x > threshold for x in predicted_list):
        
        # Your Account SID and Auth Token from twilio.com/console
        account_sid = 'ACf1d2234126a93f26c77602db2ff27147'
        auth_token = '37672d71f5670d565662f9621bdc27bd'
        client = Client(account_sid, auth_token)

        #the below code gets triggered when a flood is predicted

        message = client.messages.create(
            body=f"FLOOD ALERT: The {bucket.capitalize()} river is currently experiencing a high water level. Immediate action is required to prevent potential flooding in the surrounding areas. Please take necessary precautions and evacuate if necessary",
            from_ = sender,
            to = receiver
        )

        print(message.sid)



if __name__ == '__main__':
    
    try:
        file_name = sys.argv[1]
        with open(file_name) as f:
            print('///')
            json_data = json.load(f)
            print('---')
        print("JSON data: ", json_data)
        locations = {
        "indus": 'indus-predictor-model.pkl',
        "jehlum": 'jehlum-predictor-model.pkl'
        }
        threshold = {
            "indus": 1468.1819109947644,
            "jehlum": 1125.4064708236394
        }
    
        sms_sender = "+19712989615"
        sms_receiver = "+393293087726"

        for key in json_data["locations"].keys():
            query_result = query_db(key)

            if query_result.empty:
                print(f"No New Data {key.capitalize()}")

            else:
                df = preprocess_data(query_result)
                predicted_output = make_a_prediction(df,json_data["locations"][key])
                print(predicted_output)
                predicted = []
                for i in range(len(predicted_output)):
                    predicted.append(float(predicted_output[i]))
                print(predicted)   
                write_prediction(predicted,key,json_data["threshold"][key])
                #send_sms(predicted,json_data["threshold"][key],key,json_data["sms_sender"],json_data["sms_receiver"])
    except IndexError:
        print("No file name passed as an argument.")
    except FileNotFoundError:
        print("File not found.")
    
    
    
    
            