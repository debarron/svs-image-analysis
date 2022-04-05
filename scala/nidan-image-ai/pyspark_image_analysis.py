from pyspark.ml.image import ImageSchema
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from sparkdl import DeepImageFeaturizer
from pyspark.sql import Row, Column
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType, StringType, _create_row

from pyspark.ml.clustering import KMeans

import io
import PIL
from PIL import Image
import numpy

DB_NAME = "hdfs://vm0:9000/wsi/db2/dbCC.orc"

def getMode(channels):
  ocvTypes = {'CV_8UC4':24, 'CV_8U': 0, 'CV_8UC1':0, 'Undefined':-1, 'CV_8UC3':16}
  if channels == 1:
    return ocvTypes["CV_8UC1"]
  elif channels == 3:
    return ocvTypes["CV_8UC3"]
  elif channels == 4:
    return ocvTypes["CV_8UC4"]
  else:
    raise ValueError("Invalid number of channels")

def bytesToNumpy(byteArr):
  byteAsFile = io.BytesIO(bytearray(byteArr))
  pilImage = Image.open(byteAsFile)
  return numpy.asarray(pilImage)

def getImageFields():
  return ['origin', 'height', 'width', 'nChannels', 'mode', 'data']

def bytesToImage(img):
  imgArr = bytesToNumpy(img)
  height, width, nChannels = imgArr.shape
  mode = getMode(nChannels)
  data = bytearray(imgArr.astype(dtype=numpy.uint8).ravel().tobytes())
  return _create_row(getImageFields,["", height, width, nChannels, mode, data])

udf_toImage = udf(bytesToImage, ImageSchema.imageSchema['image'].dataType)

data = spark.read.orc(DB_NAME)
data.createOrReplaceTempView("data")

# Go for all the data in fieldId='img_1.svs-1'
dataset = spark.sql("select * from data where fileId='img_1.svs-1'")
dataset = dataset.withColumn("img", udf_toImage("bytes"))

# Divide to train and test
(train, test) = dataset.randomSplit([0.7, 0.3], 1)

featInceptionV3 = DeepImageFeaturizer(inputCol="img", outputCol="features", modelName="InceptionV3")
featXception = DeepImageFeaturizer(inputCol="img", outputCol="features", modelName="Xception")
featResNet50 = DeepImageFeaturizer(inputCol="img", outputCol="features", modelName="ResNet50")
featVGG16 = DeepImageFeaturizer(inputCol="img", outputCol="features", modelName="VGG16")
featVGG19 = DeepImageFeaturizer(inputCol="img", outputCol="features", modelName="VGG19")

feats = {
    "InceptionV3":featInceptionV3, 
    "Xception":featXception,
    "ResNet50":featResNet50,
    "VGG16":featVGG16,
    "VGG19":featVGG19
    }

models = {}
for (name, featurizer) in feats.items():
  cluster = KMeans(k=100, seed=1)
  p = Pipeline(stages=[featurizer, cluster])
  models[name] = (p.fit(train))

stats = map(lambda (name, m): (name, m.transform(test)), models.items())

