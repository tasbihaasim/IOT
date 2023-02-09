import csv
import re

# import pandas as pd

url = 'http://www.wapda.gov.pk/index.php/river-flow-data'
link = "http://www.wapda.gov.pk/index.php/river-flow-data"
dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)

dates = dfs[0][0]

column_names = {'inflow':0, 'outflow':0, 'level':0, 'humidity1':0,'temperature1':0,'humidity2':0,'temperature2':0}
df_indus = []
df_jehlum = []

for i in dates:
    df_jehlum.append({})
    df_indus.append({})


## dictionary  indus
## date is the key
## values

# ['Jehlum', 'outflow', 'sensor1'] 0.1
# ['Jehlum', 'outflow', 'sensor1'] 0.1

iterator = 0
with open('rawdata.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)

    # Iterate over the rows of the CSV file
    for row in reader:
        t = tuple(row)
        row = re.split(r'[\/_]', t[0]) ## [ list of three items ]
        #print(row, t[1])
        if row[0]=='Jehlum':
            measure = str(row[1]) + "_"+ str(row[2])
            df_jehlum[iterator][measure] = t[1]
            iterator = iterator + 1
        if row[0]=='Indus':
            measure = str(row[1]) + "_"+ str(row[2])
            df_indus[iterator][measure] = t[1]
            iterator = iterator + 1
        if (iterator%len(dates)) == 0:
            iterator = 0


months_ = []
months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

for i in dates:
    m = i[len(i)-3] + i[len(i)-2] + i[len(i)-1]
    print(months[m])
    months_.append(months[m])
    

df_indus = pd.DataFrame(df_indus)
df_jehlum = pd.DataFrame(df_jehlum)

df_indus.insert(0, 'Months', months_, True)
df_jehlum.insert(0, 'Months', months_, True)

df_jehlum = df_jehlum.reindex(columns=df_indus.columns)

print(df_jehlum)
print(df_indus)
print(len(dates))  
print(len(df_jehlum))
print(len(df_indus))





