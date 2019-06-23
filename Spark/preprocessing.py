#!/usr/bin/env python3#
#

from __future__ import print_function
import sys
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from pyspark.sql import SparkSession




def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    spark_session = SparkSession.builder.appName("stocks_monitoring").getOrCreate()
    sc = spark_session.sparkContext
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, batch_duration)
    #sqlContext = SQLContext(sc)

    topic = 'rawDBGData'
    partition = 0
    start = 0
    topicpartition = TopicAndPartition(topic, partition)
    fromoffset = {topicpartition: int(start)}
    #parse the row into separate components
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.6:9092'
    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    [topic], {'metadata.broker.list':
                    kafka_ips}, fromOffsets = fromoffset)


    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                [topic], {'metadata.broker.list':
    #                kafka_ips})

    #parse the row into separate components
    kafkaStream = kafkaStream.window(5)
    filteredStream = kafkaStream.flatMap(lambda line: line[1].split("^")).pprint()
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
