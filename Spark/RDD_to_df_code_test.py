#Spark preprocessing code.
from __future__ import print_function

import sys
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession


def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


def process(time, rdd):
    """
    This function should convert RDD to dataframe
    """
    print("========= %s =========" % str(time))

    try:
        # Get the singleton instance of SparkSession
        spark = getSparkSessionInstance(rdd.context.getConf())

        # Convert RDD[String] to RDD[Row] to DataFrame
        rowRdd = rdd.map(lambda w: Row(word=w))
        wordsDataFrame = spark.createDataFrame(rowRdd)

        # Creates a temporary view using the DataFrame.
        wordsDataFrame.createOrReplaceTempView("words")

        # Do word count on table using SQL and print it
        wordCountsDataFrame = \
            spark.sql("select word, count(*) as total from words group by word")
        wordCountsDataFrame.show()
    except:
        pass

if __name__ == "__main__":
    #if len(sys.argv) != 3:
    #    print("Usage: sql_network_wordcount.py <hostname> <port> ", file=sys.stderr)
    #    exit(-1)
    #host, port = sys.argv[1:]
    sc = SparkContext(appName="PythonSqlNetworkWordCount")
    ssc = StreamingContext(sc, 5)
    #sc.setCheckpointDir("hdfs://master:9000/RddCheckPoint")
    #ssc.checkpoint(checkpointDirectory)  a# set checkpoint directory
    #context = StreamingContext.getOrCreate(checkpointDirectory, functionToCreateContext)
    topic = 'rawDBGData'
    partition = 0
    start = 0
    topicpartition = TopicAndPartition(topic, partition)
    fromoffset = {topicpartition: int(start)}
    #parse the row into separate components

    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    ['rawDBGData'], {'metadata.broker.list':
                    '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.4:9092'}, fromOffsets = fromoffset)

    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                ['rawDBGData'], {'metadata.broker.list':
    #                '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.4:9092'})

    #parse the row into separate components

    kafkaStream = kafkaStream.window(5)
    filteredStream = kafkaStream.flatMap(lambda line: line[1].split("^"))
    

    filteredStream.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
