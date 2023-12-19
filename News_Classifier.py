from __future__ import print_function

import findspark
findspark.init()

import sys
import numpy as np
from pyspark.sql import functions as F

from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import lower, lit
from pyspark.ml.feature import IDF, Tokenizer, CountVectorizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import LinearSVC
from pyspark.ml.classification import GBTClassifier
from pyspark.ml import Pipeline
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.classification import NaiveBayes


     #Define metrics for model
def metrics(ml_model,test_data):
     predictions = ml_model.transform(test_data).cache()
     predictionAndLabels = predictions.select("label","prediction").rdd.map(lambda x: (float(x[0]), float(x[1]))).cache()
 

     metrics = MulticlassMetrics(predictionAndLabels)
 
     # Overall statistics
     precision = metrics.precision(1.0)
     recall = metrics.recall(1.0)
     f1Score = metrics.fMeasure(1.0)
     
     print("Precision:", precision)
     print("Recall:", recall)
     print("F1:", f1Score)
     print("Confusion Matrix: \n", metrics.confusionMatrix().toArray().astype(int))

if __name__ == "__main__":
    
    sc = SparkContext(appName="Assignment-5")
    spark = SparkSession(sc)
    
	#Headlines datasets
    climate_data = spark.read.option("header", True).csv(sys.argv[1])
    other_data = spark.read.option("header", True).csv(sys.argv[2]) 	
    
    #Climate headlines
    climate_data = climate_data.select(lower("Headline")).withColumnRenamed("lower(Headline)", "Headline")
    climate_data = climate_data.distinct()
    print("Climate headlines count: ", climate_data.count())
    #Clean: remove non-letters
    climate_data = climate_data.withColumn("Headline", F.regexp_replace("Headline", r"[^a-zA-Z ]", ""))
    #Remove words with 1 or 2 characters
    climate_data = climate_data.withColumn("Headline", F.regexp_replace("Headline", r"\b\w{1,2}\b", ""))
    #Remove blank headlines
    climate_data = climate_data.filter(climate_data.Headline != "")
    #Add label
    climate_data = climate_data.withColumn("label", lit(1))

    #Other headlines
    other_data = other_data.select(lower("Headline")).withColumnRenamed("lower(Headline)", "Headline")
    other_data = other_data.distinct()
    print("Other headlines count: ", other_data.count())
    #Clean: remove non-letters
    other_data = other_data.withColumn("Headline", F.regexp_replace("Headline", r"[^a-zA-Z ]", ""))
    #Remove words with 1 or 2 characters
    other_data = other_data.withColumn("Headline", F.regexp_replace("Headline", r"\b\w{1,2}\b", ""))
    #Remove blank headlines
    other_data = other_data.filter(other_data.Headline != "")
    #Add label
    other_data = other_data.withColumn("label", lit(0))
    
    #Combine climate and other headlines
    all_data = climate_data.union(other_data)
    print("Combined data count: ", all_data.count())
    
    #Split into train and test
    train, test = all_data.randomSplit(weights=[0.8, 0.2], seed=27)


    print("Train count: ", train.count(), "\nTrain grouping: ")
    train.groupBy("label").count().show()
    print("Test count: ", test.count(), "\nTest grouping: ")
    test.groupBy("label").count().show()
    
    #Weights
    p_weight = train.filter("label == 1").count() / train.count()
    print("p_weight: ", p_weight)
    n_weight = train.filter("label == 0").count() / train.count()
    print("n_weight: ", n_weight)
    train = train.withColumn("Weight", F.when(F.col("label")==1, n_weight).otherwise(p_weight))
    
    #Tokenize 
    tokenizer = Tokenizer(inputCol="Headline", outputCol="words")
    #Remove stop words
    remover = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="filtered")
    #Count vectorizer
    countVectorizer = CountVectorizer(inputCol=remover.getOutputCol(), outputCol="rawFeatures", vocabSize = 5000)
    #IDF
    idf = IDF(inputCol=countVectorizer.getOutputCol(), outputCol="featuresIDF")
    #Preprocessing pipeline
    preprocess_pipeline = Pipeline(stages=[tokenizer,remover, countVectorizer, idf])
    #Apply
    preprocess_model = preprocess_pipeline.fit(train)
    
    #Transform data
    train_transform = preprocess_model.transform(train)
    train_transform.cache()
    
    test_transform = preprocess_model.transform(test)
    test_transform.cache()
    
    #Print first 10 vocabs
    vocab = np.array(preprocess_model.stages[2].vocabulary)
    print(vocab[1:11])

    #Logistic regression
    LR_classifier = LogisticRegression(maxIter=50, regParam=0.2, featuresCol = "featuresIDF", weightCol="Weight")
    LR_pipeline = Pipeline(stages=[LR_classifier])
    LR_model = LR_pipeline.fit(train_transform)
    print("Logistic regression performance metrics: ")
    metrics(LR_model, test_transform)
    

    #GBTClassifier
    GBT_classifier = GBTClassifier(maxIter=100, featuresCol = "featuresIDF", weightCol="Weight", maxDepth=6)
    GBT_pipeline = Pipeline(stages=[GBT_classifier])
    GBT_model = GBT_pipeline.fit(train_transform)
    print("GBT classifier performance metrics: ")
    metrics(GBT_model,test_transform)
   
    #SVM
    SVM_classifier = LinearSVC(maxIter=100, regParam=0.3, featuresCol = "featuresIDF", weightCol="Weight")
    SVM_pipeline = Pipeline(stages=[SVM_classifier])
    SVM_model = SVM_pipeline.fit(train_transform)
    print("SVM classifier performance metrics: ")
    metrics(SVM_model,test_transform)
    
    #Naive Bayes
    NB = NaiveBayes(modelType = "multinomial", smoothing = 3.0, featuresCol = "featuresIDF", weightCol = "Weight")
    NB_model = NB.fit(train_transform)
    print("Naive Bayes classifier performance metrics: ")
    metrics(NB_model, test_transform)

    sc.stop()

    


















