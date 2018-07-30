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
df_input.rename(columns={
    0: 'Sentiment',
    1: 'SentimentText'
},
    inplace=True
)
df_input.to_csv('traning_dataset.csv', index=False)
