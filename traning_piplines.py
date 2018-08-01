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

df_input = pd.read_csv('data/traning_dataset2.csv', encoding='ISO-8859-1')

data = df_input['SentimentText']
label = df_input['Sentiment']
print(data.head(10))
print(label.head(10))

indexs = random.sample(range(len(df_input)), len(df_input))
data = data[indexs]
label = label[indexs]
print(data.shape)

# Clead data
print("_________________________________")
print(data.head(15))
data = cleanText(data)
print("_________________________________")
print(data.head(15))
print("_________________________________")

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.33,
                                                    random_state=42)

count_vect = CountVectorizer(max_features=5000, lowercase=True, ngram_range=(3, 6), analyzer="word")
selectKBest = SelectKBest(chi2, k=2000)
truncatedSVD = TruncatedSVD(n_components=3000, n_iter=7, random_state=42)
combined_features = FeatureUnion([("chi2", truncatedSVD), ("univ_select", selectKBest)])
dense_transformer = DenseTransformer()

clf_LG = Pipeline([
    ('count_v', count_vect),
    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('lgc', DecisionTreeClassifier())])

clf_NB = Pipeline([
    ('count_v', count_vect),
    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('lnb', GaussianNB())])

clf_SVC = Pipeline([
    ('count_v', count_vect),
    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('svc', LinearSVC(C=0.75, random_state=0, max_iter=500))])

clf_vot = Pipeline([['lnb', VotingClassifier(estimators=[('plgc', clf_LG), ('pnbc', clf_NB), ('psvc', clf_SVC)])]])

print("Create model")
clf_vot = clf_vot.fit(X_train, y_train)
print("fit Model")
prd_ = clf_vot.predict(X_test)
print("Predict data Model")
# print(prd_)
# print("transform Model")
# pred_ = list()
# for x, y, z in prd_:
#     if x == y:
#         pred_.append(x)
#     elif y == z:
#         pred_.append(y)
#     elif x == z:
#         pred_.append(z)
#     else:
#         pred_.append(x)
#
joblib.dump(clf_vot, 'tweet_analyzer.pkl')
print('Save PipeLine')
print(accuracy_score(y_test, prd_))
