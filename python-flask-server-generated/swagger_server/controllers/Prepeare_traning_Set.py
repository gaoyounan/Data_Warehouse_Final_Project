import pandas as pd
import numpy as np

inputFiles = 'data/airline_dataset.csv'

df_input = pd.read_csv(inputFiles, encoding='utf-8')

# count = 0
# print(df_input.shape)
#
# df_input = df_input.drop(df_input.columns[1], axis=1)
# df_input = df_input.drop(df_input.columns[1], axis=1)
# df_input = df_input.drop(df_input.columns[1], axis=1)
#
# print(df_input.shape)
# df_input.columns = ['Sentiment', 'SentimentText']
# df_input = df_input.replace(0, -1)
# df_input = df_input.replace(2, 0)
# df_input = df_input.replace(4, 1)

print(df_input.head(15))
df_input = df_input.drop(df_input.columns[0], axis=1)
for index, row in df_input.iterrows():
    if df_input.iloc[index, 0] == 'neutral':
        df_input.iloc[index, 0] = 0
    if df_input.iloc[index, 0] == 'positive':
        df_input.iloc[index, 0] = 1
    if df_input.iloc[index, 0] == 'negative':
        df_input.iloc[index, 0] = -1
print(df_input.head(15))
df_input.to_csv('data/traning_dataset2.csv', index=False)
