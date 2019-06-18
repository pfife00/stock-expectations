#!/usr/bin/env python
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.sql import SQLContext
#import psycopg2

def main():
    #Create spark job and name it
    sc = SparkContext(appName = 'updated_testjob')
    #Prevent spark from displaying all logs messages
    #sc.setLogLevel('Error')
    #Provides methods used to create Dstreams from various input source
    #Note: metadata.broker.list might be depreciated and need to be replaced
    #with bootstrap.servers
    ssc = StreamingContext(sc, 5)
    #set offsets
    topic = 'rawDBGData'
    partition = 0
    start = 0
    topicpartition = TopicAndPartition(topic, partition)
    fromoffset = {topicpartition: int(start)}
    #parse the row into separate components
    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                ['rawDBGData'], {'metadata.broker.list':
    #                'ec2-50-112-13-159.us-west-2.compute.amazonaws.com:9092'})
    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    ['rawDBGData'], {'metadata.broker.list':
                    'ec2-35-163-92-177.us-west-2.compute.amazonaws.com:9092, ec2-50-112-13-159.us-west-2.compute.amazonaws.com:9092, ec2-54-149-111-92.us-west-2.compute.amazonaws.com:9092'}, fromOffsets = fromoffset)
    #parse the row into separate components
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))
    filteredStream.pprint()
    #identify the stocks that we would like to buy (those with increasing price) and calculate number of shares to purchase
    buy = filteredStream.filter(lambda line: (float(line[11]) - float(line[8])) > 0.0).map(lambda line: [line[1], line[6], line[7], line[8], int(1000*(float(line[11]) - float(line[8]))/float(line[8]))]).filter(lambda line: line[4] > 0)
    #buy.pprint()

    #sqlContext = SQLContext(sc)
    #sqlContext.show()
    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
        main()
