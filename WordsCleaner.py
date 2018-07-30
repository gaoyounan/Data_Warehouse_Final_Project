from pyspark import keyword_only  ## < 2.0 -> pyspark.ml.util.keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

import re


class WordCleaner(Transformer,PysparkReaderWriter, HasInputCol, HasOutputCol):
    @keyword_only
    def __init__(self, inputCol=None, outputCol=None):
        super(WordCleaner, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def getParamsAsListOfStrings(self):
        paramValuesAsStrings = []
        return paramValuesAsStrings

    @classmethod
    def createAndInitialisePyObj(cls, paramsAsListOfStrings):
        py_obj = cls()
        py_obj.setStringParam(paramsAsListOfStrings[0])
        py_obj.setListOfStringsParam(paramsAsListOfStrings[1].split(","))
        py_obj.setIntParam(int(paramsAsListOfStrings[2]))
        return py_obj

    def _transform(self, dataset):
        def f(s):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", s).split()).lower().split()

        t = ArrayType(StringType())
        out_col = self.getOutputCol()
        in_col = dataset[self.getInputCol()]
        return dataset.withColumn(out_col, udf(f, t)(in_col))
