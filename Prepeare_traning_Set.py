import pandas as pd

inputFiles = 'data/training.1600000.processed.noemoticon.csv'
outputFile = 'data/traning1_1dataset.csv'

df_input = pd.read_csv(inputFiles, encoding='utf-8')
df_output = pd.read_csv(outputFile, encoding='utf-8')
count = 0
print(df_output.shape)
for index, row in df_input.iterrows():
    r = ''
    if row[0] == "0":
        r = [[row[1], "negative", row[4]]]
    if row[0] == "2":
        r = [[row[1], "neutral", row[4]]]
    if row[0] == "4":
        r = [[row[1], "positive", row[4]]]

    df_output.append(r, ignore_index=True)
    count += 1
    if count == 100:
        break
print(df_output.shape)
