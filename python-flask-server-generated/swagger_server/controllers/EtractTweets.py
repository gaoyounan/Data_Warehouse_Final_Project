import tweepy
import re
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import random
import time
import matplotlib.pyplot as plt

import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

from sklearn.externals import joblib
from swagger_server.controllers.StringCleaner import cleanText
import pandas as pd


def get_tweet(tweet):
    text = tweet.text
    if hasattr(tweet, 'extended_tweet'):
        text = tweet.extended_tweet['full_text']
    return [str(tweet.user.id), tweet.user.screen_name, clean_str(text)]


def clean_str(string):
    """
    Tokenization/string cleaning.
    """
    # string = re.sub(ur'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "", string, re.I | re.U)
    string = re.sub(r"\n|\t", " ", string)
    # string = re.sub(r"(.)\1{2,}", r"\1\1", string)
    # string = re.sub(r"(..)\1{2,}", r"\1\1", string)
    # string = re.sub(r"(...)\1{2,}", r"\1\1", string)
    # string = re.sub(r"(....)\1{2,}", r"\1\1", string)
    return string


class model_pipline:
    pipeline_model = None

    def __init__(self) -> None:
        super().__init__()
        self.filename = "/home/ubuntu/Data_Warehouse_Final_Project/python-flask-server-generated/pipelineModel/tweet_analyzer.pkl"
        self.pipeline_model = joblib.load(self.filename)

    def predic_data(self, data_old):
        data = cleanText(data_old)
        print(data_old)
        print(data)

        if data is None:
            data = data_old
        data = pd.Series([data])
        prd_ = self.pipeline_model.predict(data)
        return prd_


def sentiment_analysis(data):
    model = model_pipline()
    return int(model.predic_data(data)[0])


def generateESData(tweet):
    doc = {}
    doc['tweet_id'] = tweet.id_str
    doc['created_at'] = tweet.created_at
    doc['in_reply_to_status_id_str'] = tweet.in_reply_to_status_id_str
    doc['lang'] = tweet.lang
    doc['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
    doc['in_reply_to_user_id_str'] = tweet.in_reply_to_user_id_str
    doc['retweet_count'] = tweet.retweet_count
    doc['text'] = tweet.text
    doc['favorite_count'] = tweet.favorite_count
    doc['sentiment_result'] = sentiment_analysis(tweet.text)
    doc['timestamp'] = datetime.now()
    doc['screen_name'] = tweet.user.screen_name
    doc['popular_num'] = tweet.retweet_count + tweet.favorite_count

    return doc


_settings = {
    "index": {
        "blocks": {
            "read_only_allow_delete": "false"
        }
    }
}


def extractTweets(status_id, duration, interval):
    for times in range(duration):
        consumer_key = "GG1MmGFXWbVEvjAz5thB5EQDs"
        consumer_secret = "NG0nsSsy0Iu29RKVr2z3hSiL4HcwcHievXfE8Qw4r6x77AdPd0"
        access_token = "1002349562093363200-O5m7LI30kIMuruS9U2tCs06zza2711"
        access_token_secret = "i0o8KPVxU6pIRcrmzW60vmpJ1CbS6oib9IXDt28tgpqXP"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        tweet = api.get_status(status_id)
        actions = []
        tweet_id = tweet.id

        action = {
            "_index": "tweet_status_index",
            "_type": "_doc",
            "_id": tweet_id,
            "_source": generateESData(tweet)
        }
        actions.append(action.copy())

        user = tweet.user.screen_name
        max_id = None

        query = 'to:' + user

        print("------------query:" + query)
        replies = api.search(q=query, since_id=tweet_id, max_id=max_id, count=100)
        print("---------------since_id:", str(tweet_id))
        print("---------------length:", str(len(replies)))
        num = 0
        for reply in replies:
            print("---------------in_reply_to_status_id:", str(reply.in_reply_to_status_id))
            print("---------------status_id:", str(reply.in_reply_to_status_id))
            if reply.in_reply_to_status_id == int(status_id):
                reply_id = reply.id
                replyAction = {
                    "_index": "tweet_status_index",
                    "_type": "_doc",
                    "_id": reply_id,
                    "_source": generateESData(reply)
                }

                actions.append(replyAction.copy())

                print(reply.id)
                print(reply.created_at)
                print(reply.text)
                num = num + 1

                # tweet = get_tweet(reply)
                # client_socket.send((tweet[2] + "\n").encode('utf-8'))
        print(num)

        es = Elasticsearch("http://54.224.246.198:9200/")
        es.indices.create(index="_settings", body=_settings.copy())
        res = bulk(es, actions)
        es.indices.refresh(index="tweet_status_index")
        sentimentStatistics(es, status_id)
        uploadImagetoCloudinary(status_id)

        times = times + 1
        if times < duration:
            time.sleep(interval)


def sentimentStatistics(es, status_id):
    queryBody = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"in_reply_to_status_id_str": status_id}}
                ]
            }
        },
        "size": "0",
        "aggregations": {
            "by_sentiment": {
                "terms": {
                    "field": "sentiment_result"
                }
            }
        }
    }
    res = es.search(index="tweet_status_index", body=queryBody.copy())
    dict = {}
    print("==================Sentiment Analysis Distribution==================")
    for bucket in res['aggregations']['by_sentiment']['buckets']:
        dict[str(bucket['key'])] = bucket['doc_count']
        print("key:%(key)d doc_count:%(doc_count)d" % bucket)

    labels = 'Positive', 'Neutural', 'Negative'

    sizes = [];
    if '1' in dict:
        sizes.append(dict['1'])
    else:
        sizes.append(0)

    if '0' in dict:
        sizes.append(dict['0'])
    else:
        sizes.append(0)

    if '-1' in dict:
        sizes.append(dict['-1'])
    else:
        sizes.append(0)

    explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(
        "/home/ubuntu/Data_Warehouse_Final_Project/python-flask-server-generated/swagger_server/controllers/image/" + str(
            status_id) + '.png')
    # plt.savefig(
    #         "/Users/gaoyounan/Desktop/Summer Term/Data Management/final_project/Code/Data_Warehouse_Final_Project/python-flask-server-generated/swagger_server/controllers/image/" + str(
    #                 status_id) + '.png')


def uploadImagetoCloudinary(status_id):
    cloudinary.config(
        cloud_name="mxyzdl123",
        api_key="978139117644534",
        api_secret="F_mpzRKVelD61h5Paet2Gmp7iD4"
    )

    result = cloudinary.uploader.upload(
        "/home/ubuntu/Data_Warehouse_Final_Project/python-flask-server-generated/swagger_server/controllers/image/" + str(
            status_id) + '.png', public_id=str(status_id))
    # result = cloudinary.uploader.upload("/Users/gaoyounan/Desktop/Summer Term/Data Management/final_project/Code/Data_Warehouse_Final_Project/python-flask-server-generated/swagger_server/controllers/image/" + str(status_id) + '.png', public_id=str(status_id))


if __name__ == '__main__':
    status_id = 1022150726200451072
    extractTweets(status_id, 2, 3)
    # print controller_exec(1022150726200451072, 2, 10)
