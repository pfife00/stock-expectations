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
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as sa
import psycopg2.extras
from models import Cache
from models_orig import CacheOrig

#Read config file to pass db credentials
config = configparser.ConfigParser()
config.read('dwh.cfg')
DB_NAME = config.get('DB', 'DB_NAME')
DB_USER = config.get('DB', 'DB_USER')
DB_PASSWORD = config.get('DB', 'DB_PASSWORD')
DB_HOST_NAME = config.get('DB', 'DB_HOST_NAME')
DATABASE_URI = config.get('DB', 'DATABASE_URI')

def sendToSQL(df_orig, df_convert):
    """
    This function takes the spark dataframe and the parsed GE validatin output
    as input and stores the results to PostgreSQL
    """
    #connect to db and fetch all records in portfolio
    #convert spark dataframe of original data to pandas dataset
    pdsDF = df_orig.toPandas()
    DATABASE_URI = config.get('DB', 'DATABASE_URI')

    #connect to db
    DATABASE_URI = DATABASE_URI
    engine = create_engine(DATABASE_URI)

    #This will drop all tables - be careful!!!!!!!!!!!!!!
    Cache.metadata.drop_all(engine)
    CacheOrig.metadata.drop_all(engine)

    #pass dataframe to sql
    df_convert.to_sql('validation_results', engine)
    pdsDF.to_sql('data_cache', engine)

    #query table
    rows_valid = engine.execute("select * from validation_results").fetchall()
    rows_data = engine.execute("select * from data_cache").fetchall()

def ge_validation(rdd):
    """
    This function takes rdd data, converts to spark dataframe, then converts to
    GE dataframe, runs the GE functions, and batches the data
    """
    #convert to spark df
    df = rdd.toDF()
    #rename df columns
    df = df.selectExpr("_1 as ISIN", "_2 as STOCK_TICKER", "_3 as SECURITY_DESC",
                                "_4 as SECURITY_TYPE", "_5 as CURRENCY", "_6 as SECURITY_ID",
                                "_7 as DATE", "_8 as TIME", "_9 as START_PRICE",
                                "_10 as MAX_PRICE", "_11 as MIN_PRICE", "_8 as END_PRICE",
                                "_8 as TRADED_VOLUME", "_14 as NUMBER_OF_TRADES",)

    df = df.withColumn("MAX_PRICE", df["MAX_PRICE"].cast(FloatType()))
    df = df.withColumn("MIN_PRICE", df["MAX_PRICE"].cast(FloatType()))

    #convert to GE dataframe format
    sdf = ge.dataset.SparkDFDataset(df)

    #apply expectations
    sdf.expect_column_to_exist("MAX_PRICE", result_format="SUMMARY")
    sdf.expect_column_max_to_be_between("MAX_PRICE", 1, 500, result_format="BOOLEAN_ONLY")
    sdf.expect_column_min_to_be_between("MIN_PRICE", 5, 100, result_format="BOOLEAN_ONLY")

    #Save expectations to json to load to validation
    sdf.save_expectations_config("test_json.json", discard_failed_expectations=False)
    mini_batch_suite = json.load(open('test_json.json', 'r'))

    #run GE validation function
    my_dict = sdf.validate(mini_batch_suite)

    #pass to convert to dataframe function results
    df_convert = convert_df(my_dict)

    #Pass converted dataframe from convert_df function to sql
    sendToSQL(df, df_convert)

def convert_df(my_dict):
    """
    This function takes my_dict as input, converts to a dataframe and parses
    dict items in row to columns, then removes uncessary columns
    returns new dataframe
    """
    #convert dictionary to dataframe from results column
    df1 = pd.DataFrame(my_dict["results"])
    #Parse exception_info into new columns and drop exception_info
    df1[['raised_exception', 'exception_message', 'exception_traceback']] = df1.exception_info.apply(pd.Series)
    df2 = df1.drop('exception_info', axis=1)

    #Parse expectation_config into new columns and drop expectation_config
    df2[['expectation_type', 'kwargs']] = df2.expectation_config.apply(pd.Series)
    df3 = df2.drop('expectation_config', axis=1)

    #Parse results into new columns and drop expectation_config - have to use this
    #method as result has different lengths depending on expectation
    df4 = df3.result.apply(pd.Series).merge(df3, left_index = True, right_index = True)

    #drop unecesary columns
    df5 = df4.drop(['element_count', 'missing_count', 'missing_percent', 'result', 'exception_traceback'], axis=1)

    #parse kwargs to columns
    df6 = df5.kwargs.apply(pd.Series).merge(df3, left_index = True, right_index = True)

    #drop more unecesary columns
    df7 = df6.drop(['result', 'kwargs', 'exception_traceback'], axis=1)

    lst = [df1, df2, df3, df4, df5, df6]
    del lst

    return df7

def main():
    """
    Apply ETL on Spark Stream
    """
    batch_duration = 5
    topic = "stockdataset"
    #put these ips in a separate class when do code cleanup
    kafka_ips = '10.0.0.11:9092, 10.0.0.9:9093, 10.0.0.6:9094'
    #Initiate spark session
    spark_session = SparkSession \
        .builder \
        .appName("stocks_monitoring") \
        .getOrCreate()

    sc = spark_session.sparkContext
    sc.setLogLevel("ERROR")

    #Create streaming context
    ssc = StreamingContext(sc, batch_duration)

    #read from kafka
    kafkaStream = KafkaUtils\
            .createDirectStream(ssc, [topic], {'metadata.broker.list': kafka_ips})

    sqlContext = SQLContext(sc)

    #parse the row into separate components
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))

    filteredStream.foreachRDD(ge_validation)

    ssc.start()
    ssc.awaitTermination()

    return

if __name__ == "__main__":
    main()
