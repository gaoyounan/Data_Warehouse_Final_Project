from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

from string_cleaner import cleanText

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from mlxtend.preprocessing import DenseTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import TruncatedSVD
import random
import re
from load_pipline import create_model_predict
import pandas as pd
import random

df_input = pd.read_csv('data/traning_dataset2.csv', encoding='ISO-8859-1')

data = df_input['SentimentText']
label = df_input['Sentiment']
print(data.head(10))
print(label.head(10))

indexs = random.sample(range(len(df_input)), 10)
data = data[indexs]
label = label[indexs]
print(data.shape)
output = pd.DataFrame([data, create_model_predict(data)])
print(output)
