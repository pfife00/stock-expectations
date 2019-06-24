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
    #specify batch duration and kafka ips
    batch_duration = 5
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.6:9092'

    #Specify topic, offset and partition to read from kafka - this might not be
    #necessary and so is commented out
    #topic = "stockdataset"
    #partition = 0
    #start = 0
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: int(start)}

    #Entry point to spark context
    spark_session = SparkSession \
        .builder \
        .appName("stocks_monitoring") \
        .getOrCreate()
    #set spark context
    sc = spark_session.sparkContext
    #Entry pont to spark streaming context
    ssc = StreamingContext(sc, batch_duration)

    #kafka API call
    kafkaStream = KafkaUtils\
                    .createDirectStream(ssc, [topic], {'metadata.broker.list': kafka_ips})

    #Specify spark data window
    kafkaStream = kafkaStream.window(5)
    #parse the row into separate components
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))
    buy = filteredStream.filter(lambda line: (float(line[11]) - float(line[8])) > 0.0).map(lambda line: [line[1], line[6], line[7], line[8], int(1000*(float(line[11]) - float(line[8]))/float(line[8]))]).filter(lambda line: line[4] > 0)

    sqlContext = SQLContext(sc)

    #Pass RDD using foreachRDD function to process function to convert to dataframe
    filteredStream.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
