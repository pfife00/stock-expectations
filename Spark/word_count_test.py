#!/usr/bin/env python3#
#

from __future__ import print_function
import sys
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, DataFrame, SQLContext
import json
from pyspark.sql import SparkSession

def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']

# Convert RDDs of the words DStream to DataFrame and run SQL query
def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        # Get the singleton instance of SparkSession
        sqlContext = getSqlContextInstance(rdd.context)

        # Convert RDD[String] to RDD[Row] to DataFrame
        #rowRdd = rdd.map(lambda w: Row(word=w))
        rowRdd = rdd.map(lambda w: Row(word=w[0], cnt=w[1]))
        #rowRdd.pprint()
        wordsDataFrame = sqlContext.createDataFrame(rowRdd)
        wordsDataFrame.show()

        # Creates a temporary view using the DataFrame.
        wordsDataFrame.createOrReplaceTempView("words")

        # Do word count on table using SQL and print it
        wordCountsDataFrame = \
             spark.sql("select SUM(cnt) as total from words")
        wordCountsDataFrame.show()
    except:
       pass


def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    spark_session = SparkSession.builder.appName("stocks_monitoring").getOrCreate()
    sc = spark_session.sparkContext
    sqlContext = SQLContext(sc)
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, batch_duration)

    topic = 'rawDBGData'
    #partition = 200
    #start = 0
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: int(start)}
    #parse the row into separate components
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.6:9092'
    #kafkaStream = KafkaUtils.createDirectStream(ssc,
        #            [topic], {'metadata.broker.list':
        #            kafka_ips}, fromOffsets = fromoffset)


    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    [topic], {'metadata.broker.list':
                    kafka_ips})

    #parse the row into separate components

    kafkaStream = kafkaStream.window(5)
    filteredStream = kafkaStream.flatMap(lambda line: \
        line[1].split("^")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b).pprint()

    words.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
