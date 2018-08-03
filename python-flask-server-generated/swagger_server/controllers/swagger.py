from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import cloudinary.api
import json


def es_analysis(tweet_id):
    queryBody = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"tweet_id": tweet_id}}
                ]
            }
        },
        "size": "100"
    }

    # es = Elasticsearch()
    es = Elasticsearch("http://54.224.246.198:9200/")
    res = es.search(index="tweet_status_index", body=queryBody.copy())

    orginal_tweet_id = None
    orginal_created_at = None
    orginal_retweet_count = None
    orginal_favorite_count = None
    orginal_text = None

    print("==================Origninal Tweets==================")
    for hit in res['hits']['hits']:
        print("tweet_id:%(tweet_id)s "
              "created_at:%(created_at)s "
              "creator:%(screen_name)s "
              "retweet_count:%(retweet_count)d "
              "favorite_count:%(favorite_count)d "
              "text:%(text)s" % hit["_source"])
        orginal_tweet_id = hit["_source"]["tweet_id"]
        orginal_created_at = hit["_source"]["created_at"]
        orginal_retweet_count = hit["_source"]["retweet_count"]
        orginal_favorite_count = hit["_source"]["favorite_count"]
        orginal_text = hit["_source"]["text"]

    original_created_at = res['hits']['hits'][0]["_source"]["created_at"]

    queryBody = {
        "sort": [
            {"popular_num": "desc"}
        ],
        "size": "1",
        "query": {
            "term": {"in_reply_to_status_id_str": tweet_id}
        }
    }
    res = es.search(index="tweet_status_index", body=queryBody.copy())
    print("==================The most popular replies==================")
    reply_tweet_id = None
    reply_created_at = None
    reply_creator = None
    reply_retweet_count = None
    reply_favorite_count = None
    reply_text = None
    for hit in res['hits']['hits']:
        print("tweet_id:%(tweet_id)s "
              "created_at:%(created_at)s "
              "creator:%(screen_name)s "
              "retweet_count:%(retweet_count)d "
              "favorite_count:%(favorite_count)d "
              "text:%(text)s" % hit["_source"])

        reply_tweet_id = hit["_source"]["tweet_id"]
        reply_created_at = hit["_source"]["created_at"]
        reply_creator = hit["_source"]["screen_name"]
        reply_retweet_count = hit["_source"]["retweet_count"]
        reply_favorite_count = hit["_source"]["favorite_count"]
        reply_text = hit["_source"]["text"]

    queryBody = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"in_reply_to_status_id_str": tweet_id}}
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
    dictSentiment = {}
    print("==================Sentiment Analysis Distribution==================")
    for bucket in res['aggregations']['by_sentiment']['buckets']:
        dictSentiment[str(bucket['key'])] = bucket['doc_count']
        print("key:%(key)d doc_count:%(doc_count)d" % bucket)

    cloudinary.config(
        cloud_name="mxyzdl123",
        api_key="978139117644534",
        api_secret="F_mpzRKVelD61h5Paet2Gmp7iD4"
    )

    img = cloudinary.CloudinaryImage(str(tweet_id))
    # print(img.url)
    print(type(img))
    resultJson = {
        "tweet_id": orginal_tweet_id,
        "created_at": orginal_created_at,
        "retweet_count": orginal_retweet_count,
        "favorite_count": orginal_favorite_count,
        "text": orginal_text,
        "the_hottest_reply": {
            "tweet_id": reply_tweet_id,
            "creator": reply_creator,
            "created_at": reply_created_at,
            "retweet_count": reply_retweet_count,
            "favorite_count": reply_favorite_count,
            "text": reply_text
        },
        "statistics_url": str(img.url)
    }

    # dictMerged1 = dict(resultJson.items() + dictSentiment.items())
    dictMerged1 = {**resultJson, **dictSentiment}
    result = json.dumps(dictMerged1)
    return result

#
# tweet_id = "1022150726200451072"
# print()
# es_analysis(tweet_id)
