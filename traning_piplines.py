from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word

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

df_input = pd.read_csv('data/traning_dataset.csv', encoding='ISO-8859-1')

data = df_input['SentimentText']
label = df_input['Sentiment']

indexs = random.sample(range(len(df_input)), 100000)
data = data[indexs]
label = label[indexs]

# Clead data
print("_________________________________")
print(data.head(15))
for x, index in data.iteritems():
    x = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(x)).split()).lower().split()
print(data.head(15))
print("_________________________________")
stop = stopwords.words('english')
data = data.str.replace('[^\w\s]', '')
data = data.apply(lambda x: " ".join(x for x in x.split() if x not in stop))
freq = pd.Series(' '.join(data).split()).value_counts()[:10]
freq = list(freq.index)
data = data.apply(lambda x: " ".join(x for x in x.split() if x not in freq))
data[:5].apply(lambda x: str(TextBlob(x).correct()))
data = data.apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
print(data.head())

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.33,
                                                    random_state=42)

count_vect = CountVectorizer(max_features=1500, lowercase=True, ngram_range=(3, 5), analyzer="word")
selectKBest = SelectKBest(chi2, k=500)
truncatedSVD = TruncatedSVD(n_components=1000, n_iter=7, random_state=42)
combined_features = FeatureUnion([("chi2", truncatedSVD), ("univ_select", selectKBest)])
dense_transformer = DenseTransformer()

clf_LG = Pipeline([
    ('count_v', count_vect),
#    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('lgc', DecisionTreeClassifier())])

clf_NB = Pipeline([
    ('count_v', count_vect),
#    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('lnb', GaussianNB())])

clf_SVC = Pipeline([
    ('count_v', count_vect),
#    ('features', combined_features),
    ('to_dens', DenseTransformer()),
    ('svc', LinearSVC(C=0.75, random_state=0, max_iter=500))])

clf_vot = Pipeline([['lnb', VotingClassifier(estimators=[('plgc', clf_LG), ('pnbc', clf_NB), ('psvc', clf_SVC)])]])

print("Create model")
clf_vot = clf_vot.fit(X_train, y_train)
print("fit Model")
prd_ = clf_vot.transform(X_test)
# print(prd_)
print("transform Model")
pred_ = list()
for x, y, z in prd_:
    if x == y:
        pred_.append(x)
    elif y == z:
        pred_.append(y)
    elif x == z:
        pred_.append(z)
    else:
        pred_.append(x)

joblib.dump(clf_vot, 'tweet_analyzer.pkl')
print(accuracy_score(y_test, pred_))
