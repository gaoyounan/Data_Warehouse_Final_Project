import re, string
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob import Word
import pandas as pd


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def cleanText(data):
    for index, x in data.iteritems():
        data[index] = strip_all_entities(strip_links(x))
    stop = stopwords.words('english')
    data = data.str.replace('[^\w\s]', '')
    data = data.apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    freq = pd.Series(' '.join(data).split()).value_counts()[:10]
    freq = list(freq.index)
    data = data.apply(lambda x: " ".join(x for x in x.split() if x not in freq))
    data = data.apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    return data
