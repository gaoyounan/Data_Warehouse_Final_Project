import connexion
import six
from sklearn.externals import joblib
from swagger_server.controllers.StringCleaner import cleanText
import pandas as pd
import random
from swagger_server import util


class model_pipline:
    pipeline_model=None
    def __init__(self) -> None:
        super().__init__()
        self.filename = "/home/ubuntu/Data_Warehouse_Final_Project/python-flask-server-generated/pipelineModel/tweet_analyzer.pkl"
        self.pipeline_model = joblib.load(self.filename)

    def predic_data(self, data_old):
        data = cleanText(data_old)
        for index, row in data.iteritems():
            if row is None:
                data[index] = data_old[index]
        prd_ = self.pipeline_model.predict(data)
        return prd_


def create_model_predict(data):
    model = model_pipline()
    return model.predic_data(data)


def get_result_tweet_id(itemid):  # noqa: E501
    """predict the salses

    Returns a single number for the salse # noqa: E501

    :param itemid: ID of item to return
    :type itemid: int

    :rtype: None
    """
    """
    this just for testing
    """
    df_input = pd.read_csv("/home/ubuntu/Data_Warehouse_Final_Project/data/traning_dataset2.csv", encoding='ISO-8859-1')

    data = df_input['SentimentText']
    label = df_input['Sentiment']

    indexs = random.sample(range(len(df_input)), 10)
    data = data[indexs]
    label = label[indexs]

    print(data.shape)

    prd = create_model_predict(data)
    prd = pd.Series(prd)
    data = pd.Series(data.values)
    output = pd.concat([data, prd], axis=1)
    html = output.to_html('filename.html')
    """
    End of test
    """
    """
    html = "<html>" \
           "<head><title>Tweet Analyzer</title></head>" \
           "<body><h1>Tweet Analyzer</h1>" \
           "<h3>Coming Soon</h3>" \
           "<h3>" + output + "</h3>" \
                                    "</body>" \
                                    "</html>"
    """
    return html


def set_tweet_id(itemid):  # noqa: E501
    """predict the salses

    Returns a single number for the salse # noqa: E501

    :param itemid: ID of item to return
    :type itemid: int

    :rtype: None
    """
    html = "<html>" \
           "<head><title>Tweet Analyzer</title></head>" \
           "<body><h1>Tweet Analyzer</h1>" \
           "<h3>Coming Soon</h3></body>" \
           "</html>"
    return html
