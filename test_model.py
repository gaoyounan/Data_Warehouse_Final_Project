from load_pipline import create_model_predict
import pandas as pd
import random

df_input = pd.read_csv("/home/ubuntu/Data_Warehouse_Final_Project/data/traning_dataset2.csv", encoding='ISO-8859-1')

data = df_input['SentimentText']
label = df_input['Sentiment']

indexs = random.sample(range(len(df_input)), 10)
data = data[indexs]
label = label[indexs]

print(data.shape)

prd=create_model_predict(data)
prd=pd.Series(prd)
data=pd.Series(data.values)
output = pd.concat([data,prd ],axis=1)

print(output)
