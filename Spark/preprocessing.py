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
from pyspark.sql import SparkSession, SQLContext
import ConfigParser
import psycopg2


#Read config file to pass db credentials
config = ConfigParser.ConfigParser()
config.read('dwh.cfg')
DB_NAME = config.get('DB', 'DB_NAME')
DB_USER = config.get('DB', 'DB_USER')
DB_PASSWORD = config.get('DB', 'DB_PASSWORD')

def sendToSQL(rdd):
        #connect to db and fetch all records in portfolio
        postgres_ip = "10.0.0.4"
        #create connection to database
        connection = psycopg2.connect(host = postgres_ip, database = DB_NAME, user = DB_USER, password = DB_PASSWORD)
        #Allow Python code to execute PostgreSQL command in a database session
        cursor = connection.cursor()
        #Execute a database operation (query or command)
        cursor.execute('SELECT * FROM portfolio')
        #Fetch all (remaining) rows of a query result, returning them as a list
        #of tuples. An empty list is returned if there is no more record to fetch.
        postgres = cursor.fetchall()

        #for each sell order in current rdd
        for line in rdd:
                for row in postgres:
                        #if the stock is owned, record the transaction and remove the stock from your portfolio
                        if line[0] == row[0]:
                                query = 'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s)'
                                data = (line[0], line[1], line[2], line[3], -1*int(row[2]))
                                cursor.execute(query, data)
                                query = 'DELETE FROM portfolio WHERE ticker = %s'
                                data = (line[0],)
                                cursor.execute(query, data)
                                break;
        connection.commit()
        connection.close()


def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    #Initiate spark session
    spark_session = SparkSession \
        .builder \
        .appName("stocks_monitoring") \
        .getOrCreate()

    sc = spark_session.sparkContext
    sc.setLogLevel("ERROR")

    #Create streaming context
    ssc = StreamingContext(sc, batch_duration)
    #sqlContext = SQLContext(sc)

    topic = "stockdataset"
    #partition = 0
    #start = 0
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: int(start)}
    #parse the row into separate components
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9092, 10.0.0.6:9092'
    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                [topic], {'metadata.broker.list':
    #                kafka_ips}, fromOffsets = fromoffset)

    #read from kafka
    kafkaStream = KafkaUtils\
                    .createDirectStream(ssc, [topic], {'metadata.broker.list': kafka_ips})

    #window the data
    #kafkaStream_window = kafkaStream.window(5)
    #parse the row into separate components
    #filteredStream = kafkaStream_window.flatMap(lambda line: line[1].split("^"))
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))
    buy = filteredStream.filter(lambda line: (float(line[11]) - float(line[8])) > 0.0).map(lambda line: [line[1], line[6], line[7], line[8], int(1000*(float(line[11]) - float(line[8]))/float(line[8]))]).filter(lambda line: line[4] > 0)

    sqlContext = SQLContext(sc)
    #use foreachPartition to reduce the number of database connections that are opened/closed
    #buy.foreachRDD(lambda rdd: rdd.foreachPartition(sendToSQL))

    buy.pprint()
    ssc.start()
    ssc.awaitTermination()

    return

if __name__ == "__main__":
    main()
