import tweepy
import socket
import requests
import time
import csv
import stat
import os
import socket
import json
import re
#import urllib.parse
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import random
import time

def get_tweet(tweet):
    text = tweet.text
    if hasattr(tweet, 'extended_tweet'):
            text = tweet.extended_tweet['full_text']
    return [str(tweet.user.id),tweet.user.screen_name, clean_str(text)]


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


def sentiment_analysis():
        return random.randint(-1,1)

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
        doc['sentiment_result'] = sentiment_analysis()
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

def extractTweets(status_id, duration):


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

                replies = api.search(q=query, since_id=tweet_id, max_id=max_id, count=100)
                num = 0
                for reply in replies:
                        if reply.in_reply_to_status_id == status_id:
                                reply_id = reply.id
                                replyAction = {
                                        "_index": "tweet_status_index",
                                        "_type": "_doc",
                                        "_id": reply_id,
                                        "_source": generateESData(reply)
                                }

                                actions.append(replyAction.copy())

                                print reply.id
                                print reply.created_at
                                print reply.text
                                num = num + 1

                                # tweet = get_tweet(reply)
                                # client_socket.send((tweet[2] + "\n").encode('utf-8'))
                print num

                es = Elasticsearch()
                es.indices.create(index="_settings", body=_settings.copy())
                res = bulk(es, actions)
                es.indices.refresh(index="tweet_status_index")
                times = times + 1
                if times < duration:
                        time.sleep(300)



if __name__ == '__main__':

        status_id = 1023224248842760194
        extractTweets(status_id , 1)

        # consumer_key = "GG1MmGFXWbVEvjAz5thB5EQDs"
        # consumer_secret = "NG0nsSsy0Iu29RKVr2z3hSiL4HcwcHievXfE8Qw4r6x77AdPd0"
        # access_token = "1002349562093363200-O5m7LI30kIMuruS9U2tCs06zza2711"
        # access_token_secret = "i0o8KPVxU6pIRcrmzW60vmpJ1CbS6oib9IXDt28tgpqXP"
        #
        #
        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.secure = True
        # auth.set_access_token(access_token, access_token_secret)
        #
        # #api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
        # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        #
        # status_id = 1023224248842760194
        #
        # tweet = api.get_status(status_id)
        # actions = []
        # tweet_id = tweet.id
        #
        # action = {
        #         "_index": "tweet_status_index",
        #         "_type": "_doc",
        #         "_id": tweet_id,
        #         "_source": generateESData(tweet)
        # }
        # actions.append(action.copy())
        #
        #
        # user = tweet.user.screen_name
        # max_id = None
        #
        # query = 'to:'+user
        #
        # replies = api.search(q=query, since_id=tweet_id, max_id=max_id, count=100)
        # num = 0
        # for reply in replies:
        #     if reply.in_reply_to_status_id == status_id:
        #
        #             reply_id = reply.id
        #             replyAction = {
        #                     "_index": "tweet_status_index",
        #                     "_type": "_doc",
        #                     "_id": reply_id,
        #                     "_source": generateESData(reply)
        #             }
        #
        #             actions.append(replyAction.copy())
        #
        #             print reply.id
        #             print reply.created_at
        #             print reply.text
        #             num = num+1
        #
        #         # tweet = get_tweet(reply)
        #         # client_socket.send((tweet[2] + "\n").encode('utf-8'))
        # print num
        #
        # es = Elasticsearch()
        # es.indices.create(index="_settings", body=_settings.copy())
        # res = bulk(es, actions)
        # es.indices.refresh(index="tweet_status_index")

