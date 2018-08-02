from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

tweet_id = "1022150726200451072"

queryBody = {
  "query": {
    "bool": {
      "must": [
        { "match": { "tweet_id": tweet_id }}
      ]
    }
  },
  "size":"100"
}
es = Elasticsearch()
res = es.search(index="tweet_status_index", body=queryBody.copy())
print("==================Origninal Tweets==================")
for hit in res['hits']['hits']:
            print("tweet_id:%(tweet_id)s " 
                  "created_at:%(created_at)s " 
                  "creator:%(screen_name)s " 
                  "retweet_count:%(retweet_count)d "
                  "favorite_count:%(favorite_count)d "
                  "text:%(text)s" % hit["_source"])

queryBody = {
    "sort" : [
        { "popular_num" : "desc" }
    ],
	"size":"1",
    "query" : {
        "term" : { "in_reply_to_status_id_str": tweet_id }
    }
}
res = es.search(index="tweet_status_index", body=queryBody.copy())
print("==================The most popular replies==================")
for hit in res['hits']['hits']:
    print("tweet_id:%(tweet_id)s "
          "created_at:%(created_at)s "
          "creator:%(screen_name)s "
          "retweet_count:%(retweet_count)d "
          "favorite_count:%(favorite_count)d "
          "text:%(text)s" % hit["_source"])

queryBody = {
  "query": {
    "bool": {
      "must": [
        { "match": { "in_reply_to_status_id_str": tweet_id }}
      ]
    }
  },
  "size":"0",
  "aggregations" : {
    "by_sentiment" : {
      "terms" : {
        "field" : "sentiment_result"
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

# import matplotlib.pyplot as plt
#
# # Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'Positive', 'Neutural', 'Negative'
# sizes = [dict['1'], dict['0'], dict['-1']]
# explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
#
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.savefig('foo.png')
#plt.show()