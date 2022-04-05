from PIL import Image
import io
import numpy as np

from pyspark.ml.image import ImageSchema
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from sparkdl import DeepImageFeaturizer
from pyspark.sql import Row, Column
from pyspark.sql.functions import col, expr, when, udf
from pyspark.sql.types import IntegerType


def labelFromFileName(strPath):
	fileStr = strPath.encode("ascii", "ignore").split("/")[-1]
  if fileStr.split(".")[0] == "cat":
    return int(0)
  else:
	  return int(1)

udfLabel = udf(lambda row: labelFromFileName(row))
#---

def PIL_from_bytearr(imgByteArr):
  stream = io.BytesIO(imgByteArr)
  return Image.open(stream)

udfPIL = udf(lambda row: PIL_from_bytearr(row))
#---

def _bytesToPIL(byteArr):
  from PIL import Image
  import io
  return Image.open(io.BytesIO(byteArr))

udfBytes2PIL = udf(lambda row: _bytesToPIL(row))
#---

def _PIL2NDArray(PILImg):
  import numpy
  return numpy.array(PILImg)

udfPIL2NDArr = udf(lambda row: _PIL2NDArray(row))
#---


# Read the data
data = spark.read.orc("hdfs://vm0:9000/wsi/orc/db.orc")
data.createOrReplaceTempView("data")
imgs = spark.sql("select bytes from data where fileId='img_1.svs-1'")

imgs_1 = imgs.withColumn("PIL", udfBytes2PIL(col("bytes")))
imgs_2 = imgs_1.withColumn("NDArr", udfPIL2NDArr(col("PIL"))


images = data.withColumn("PIL", udfPIL(col("bytes"))).select("PIL")


train_df = ImageSchema.readImages("hdfs://vm0:9000/train")
test_df = ImageSchema.readImages("hdfs://vm0:9000/test")
labels = spark.read.csv("hdfs://vm0:9000/labels.txt", header=True)

train_df = train_df.withColumn("label", udfLabel(col("image.origin")).cast(IntegerType()))
the_train = train_df.randomSplit([0.8, 0.2])

featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
lr = LogisticRegression(maxIter=20, regParam=0.05, elasticNetParam=0.3, labelCol="label")
p = Pipeline(stages=[featurizer, lr])
model = p.fit(the_train[0])


# Inspect error
df = model.transform(the_train[1].limit(10)).select("image", "prediction", "label")
predictionAndLabels = df.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Training set accuracy = " + str(evaluator.evaluate(predictionAndLabels)))


image_df = ImageSchema.readImages("hdfs://vm0:9000/train_data")
labels = image_df.withColumn("id", udfTag(col("image.origin")))


