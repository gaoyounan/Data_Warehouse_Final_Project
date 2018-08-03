from sklearn.externals import joblib
from StringCleaner import cleanText
import numpy as np


class model_pipline:

    def __init__(self) -> None:
        super().__init__()
        self.filename = 'tweet_analyzer.pkl'
        self.pipeline_model = joblib.load(self.filename)

    def predic_data(self, data_old):
        data = cleanText(data_old)
        for index, row in data.iteritems():
            if row is None:
                data[index] = data_old[index]
        print(type(data))
        prd_ = self.pipeline_model.predict(data)
        return prd_


def create_model_predict(data):
    model = model_pipline()
    return model.predic_data(data)
