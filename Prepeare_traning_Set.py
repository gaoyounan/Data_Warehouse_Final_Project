import pandas as pd
import numpy as np

inputFiles = 'data/training.1600000.processed.noemoticon.csv'

df_input = pd.read_csv(inputFiles, encoding='ISO-8859-1')

count = 0
print(df_input.shape)

df_input = df_input.drop(df_input.columns[1], axis=1)
df_input = df_input.drop(df_input.columns[1], axis=1)
df_input = df_input.drop(df_input.columns[1], axis=1)
df_input = df_input.drop(df_input.columns[1], axis=1)

print(df_input.shape)
df_input.columns = ['Sentiment', 'SentimentText']
df_input = df_input.replace(0, -1)
df_input = df_input.replace(2, 0)
df_input = df_input.replace(4, 1)
df_input.to_csv('data/traning_dataset.csv', index=False)
