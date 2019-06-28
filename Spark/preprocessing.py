#!/usr/bin/env python3#
#

from __future__ import print_function
import sys
from psycopg2.extras import Json
from pandas.io.json import json_normalize
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from pyspark.sql import SparkSession, SQLContext, Row
import configparser
import great_expectations as ge
import PostgreSQLConnect
import psycopg2
import pandas as pd
#from sqlalchemy import create_engine
import psycopg2.extras

#Read config file to pass db credentials
config = configparser.ConfigParser()
config.read('dwh.cfg')
DB_NAME = config.get('DB', 'DB_NAME')
DB_USER = config.get('DB', 'DB_USER')
DB_PASSWORD = config.get('DB', 'DB_PASSWORD')

def sendToSQL(test_json):
    #connect to db and fetch all records in portfolio
    postgres_ip = '10.0.0.4'

    #print(test_json)
    #create connection to database
    #df = pd.DataFrame.from_dict(eval(test_json), orient='columns')
    #print(df)
    #connection = psycopg2.connect(host = postgres_ip, database = DB_NAME, user = DB_USER, password = DB_PASSWORD)
    #Allow Python code to execute PostgreSQL command in a database session
    #convert json to string
    #this does something
    #print(test_json['results'])
    new_json = json.dumps(test_json)
    python_obj = json.loads(new_json)
    jn = json_normalize(python_obj)
    df_columns = list(jn)
    columns = ",".join(df_columns)

    # create VALUES('%s', '%s",...) one '%s' per column
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

    #print(python_obj)
    my_data=[]
    json_fields = ['results', 'success', 'statistics']
    #this works!!!
    #connection = psycopg2.connect(host = postgres_ip, port=5432, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    #cursor = connection.cursor()
    #cursor.execute('DROP TABLE IF EXISTS json_cache;')
    #cursor.execute('DROP TABLE IF EXISTS data_table;')
    #cursor.execute('CREATE TABLE data_table(test_json json);')
    #cursor.execute('INSERT INTO data_table(results, success, statistics)'

    #for item in test_json:
        #print(test_json['results'])


    #conn = engine.raw_connection()
    #cur = conn.cursor()
    #output = io.StringIO()
    #conn.commit()
    #conn.close()
    #cursor.execute('CREATE TABLE IF NOT EXISTS data_table(results VARCHAR, success VARCHAR, statistics VARCHAR);')
    #cursor.execute('create table data_cache(test_json JSONB[]);')
    #test - delete this!!

    #query = 'INSERT INTO data_cache VALUES (%s)'
    #data = (test_json['results'])
    #print(test_json['results'])
    #for line in test_json:

    #query = 'INSERT INTO data_table VALUES (%s, %s, %s)'
    #data = (test_json['results'], test_json['success'], test_json['statistics'])
    #print(data.type())
        #    print(key, value)
    #cursor.execute(query, data)

    #for item in test_json['results']:
    #    for k,v in item.items():
    #        query = 'INSERT INTO data_table(results) VALUES (%s)'
    #        data = (2,3)
    #    cursor.execute(query, data)

    # preparing geometry json data for insertion

    with psycopg2.connect(host = postgres_ip, port=5432, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
        with conn.cursor() as cursor:
            query = """
                INSERT into
                    data_table
                    (success, exception_info, expectation_config, result)
                VALUES
                    (%(success)s, %(exception_info)s, %(expectation_config)s, %(result)s);
            """
            cursor.executemany(query, test_json)

        conn.commit()
        #my_data = {field: item[field] for field in json_fields}
        #cur.execute("INSERT INTO data_cache VALUES (%s)", (json.dumps(my_data),))
    #query = '''INSERT INTO data_cache (noaa_id, latitude, longitude, elevation, state, name) VALUES(%s,%s,%s,%s,%s,%s);'''
    #query = INSERT INTO 'data_cache' VALUES (%s, %s, %s, %s, %s)
    #cursor.execute(query, data)
    #Execute a database operation (query or command)
    #cursor.execute('SELECT * FROM data_cache')
    #Fetch all (remaining) rows of a query result, returning them as a list
    #of tuples. An empty list is returned if there is no more record to fetch.
    #postgres = cursor.fetchall()

    #for each sell order in current rdd
    #for line in rdd:
    #        for row in postgres:
                    #if the stock is owned, record the transaction and remove the stock from your portfolio
    #                if line[0] == row[0]:
    #                        query = 'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s)'
    #                        data = (line[0], line[1], line[2], line[3], -1*int(row[2]))
    #                        cursor.execute(query, data)
    #                        query = 'DELETE FROM portfolio WHERE ticker = %s'
    #                        data = (line[0],)
    #                        cursor.execute(query, data)
    #                        break;
    connection.commit()
    connection.close()

def initDbConnection():
    """
    Function to create PostgreSQL connection
    """
    conn = PostgreSQLConnect.PostgreSQLConnect()
    return conn

#def writeToPostgres(df, table, mode):
#    """
#    Function to write to PostgreSQL table
#    Note: mode is the what data input should do, for example append
#    """
#    conn.write(df, table, mode)

def ge_validation(rdd):
    df = rdd.toDF()
    #rename df columns
    df = df.selectExpr("_1 as ISIN", "_2 as STOCK_TICKER", "_3 as SECURITY_DESC",
                                "_4 as SECURITY_TYPE", "_5 as CURRENCY", "_6 as SECURITY_ID",
                                "_7 as DATE", "_8 as TIME", "_9 as START_PRICE",
                                "_10 as MAX_PRICE", "_11 as MIN_PRICE", "_8 as END_PRICE",
                                "_8 as TRADED_VOLUME", "_14 as NUMBER_OF_TRADES",)
    #df.show()

    #Not sure if I need this row
    df = df.withColumn("MAX_PRICE", df["MAX_PRICE"].cast(FloatType()))
    df = df.withColumn("MIN_PRICE", df["MAX_PRICE"].cast(FloatType()))

    #conn = initDbConnection()
    #conn.write(buy_df, "data_cache", "append")
    sdf = ge.dataset.SparkDFDataset(df)
    #print(json.dumps(sdf.expect_column_to_exist("value"))) #est, does col have value
    #print(json.dumps(sdf.expect_column_to_exist("key"))) #test, does col have key
    #print(json.dumps(sdf.expect_column_to_exist("_4"))) #test, does col have _4
    #test_json = json.dumps(sdf.expect_column_mean_to_be_between("_4", -100, 100, result_format="SUMMARY"))
    sdf.expect_column_to_exist("MAX_PRICE")
    sdf.expect_column_max_to_be_between("MAX_PRICE", 200, 500, result_format="SUMMARY")
    #sdf.expect_column_values_to_be_between("START_PRICE", 0.5, 1000, result_format="SUMMARY")
    sdf.expect_column_min_to_be_between("MIN_PRICE", 5, 100, result_format="SUMMARY")
    #sdf.expect_column_to_exist("key")
    #sdf.expect_column_to_exist("value")
    #print(test_json)
    #Save expectations to json to load to validation
    #this one is old
    sdf.save_expectations_config("test_json.json")
    mini_batch_suite = json.load(open('test_json.json', 'r'))

    json_out = sdf.validate(mini_batch_suite)

    #This works!!!!
    sendToSQL(json_out)
    #my_expectations_config = json.load(file("test_json.json"))
    #print(my_expectations_config)
    #mini_batch_suite = sdf.save_expectations_config("my_stock_expectations.json")
    #conn = initDbConnection()
    #conn.write(test_json, "data_cache", "append")
    #writeToPostgres(sdf, "data_cache", "append")
    #sdf.validate(expectations_suite=mini_batch_suite)
    #run ge_validation
    #sdf.validate(expectations_suite=mini_batch_suite)
    #try:
        #try to loop through rdd code

    #except ValueError:
    #    print("No data!!!")

def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    topic = "stockdataset"
    #put these ips in a separate class when do code cleanup
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9093, 10.0.0.6:9094'
    #kafka_ips = '10.0.0.11:9092'
    #Initiate spark session
    spark_session = SparkSession \
        .builder \
        .appName("stocks_monitoring") \
        .getOrCreate()

    sc = spark_session.sparkContext
    sc.setLogLevel("ERROR")

    #Create streaming context
    ssc = StreamingContext(sc, batch_duration)

    #partition = 0
    #start = 0
    #topicpartition = TopicAndPartition(topic, partition)
    #fromoffset = {topicpartition: int(start)}
    #parse the row into separate components

    #kafkaStream = KafkaUtils.createDirectStream(ssc,
    #                [topic], {'metadata.broker.list':
    #                kafka_ips, 'auto.offset.reset':'smallest'})

    #read from kafka
    kafkaStream = KafkaUtils\
            .createDirectStream(ssc, [topic], {'metadata.broker.list': kafka_ips})
#
    sqlContext = SQLContext(sc)
    #window the data
    #kafkaStream_window = kafkaStream.window(100)
    #parse the row into separate components
    #filteredStream = kafkaStream_window.map(lambda line: line[1].split("^"))
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))
    #buy = filteredStream.filter(lambda line: (float(line[11]) - float(line[8])) > 0.0).map(lambda line: [line[1], line[6], line[7], line[8], int(1000*(float(line[11]) - float(line[8]))/float(line[8]))]).filter(lambda line: line[4] > 0)
    #filtered = filteredStream.filter(lambda line: line[1])#, line[2], line[6], line[7],
                                        #line[8], line[9], line[10], line[11], line[12],
                                        #lin3[13], line[14])
    #filter_s = filteredStream.filter(lambda line: line[1], line[2]).pprint()
    #buy.pprint()
    #use foreachPartition to reduce the number of database connections that are opened/closed
    #buy.foreachRDD(lambda rdd: rdd.foreachPartition(sendToSQL))

    #This does not work!!!!
    #buy_df = sqlContext.createDataFrame(buy)

    #this works for real but don't need it!!!
    #buy.foreachRDD(lambda rdd: rdd.toDF().show())
    #pass to GE validation function - this works
    #filteredStream.foreachRDD(lambda rdd: rdd.foreachPartition(ge_validation))
    #buy.foreachRDD(ge_validation)
    filteredStream.foreachRDD(ge_validation)
    #this line works!!!
    #new_df = filteredStream.foreachRDD(lambda rdd: rdd.toDF())
    #print(new_df)
    #ge_validation(new_df)



    #implement jdbc
    ssc.start()
    ssc.awaitTermination()

    return

if __name__ == "__main__":
    main()
