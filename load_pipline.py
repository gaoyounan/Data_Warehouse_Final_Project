from sklearn.externals import joblib
from string_cleaner import cleanText


class model_pipline:

    def __init__(self) -> None:
        super().__init__()
        self.filename = 'tweet_analyzer.pkl'
        self.pipeline_model = joblib.load(self.filename)

    def predic_data(self, data):
        data = cleanText(data)
        prd_ = self.pipeline_model.predict(data)
        return prd_


def create_model_predict(data):
    model = model_pipline()
    return model.predic_data(data)
