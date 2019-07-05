#!/usr/bin/env python3#
#Author: Forest Pfeiffer
#Create a Kafka producer
# that reads data from a S3 bucket and sends it to a topic.

#to install boto3, run the following command:
#pip install boto3
import ConfigParser
from kafka import KafkaProducer
from json import dumps
import time
import boto3
import botocore
import pandas as pd

def main():

    #create Kafka producer that communicates with master node of ec2 instance running Kafka
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

    #read credentials from dwg.cfg file (note this file will not be stored
    #on github for security reasons)
    config = ConfigParser.ConfigParser()
    config.read('dwh.cfg')
    AWS_ACCESS_KEY_ID = config.get('AWS', 'KEY')
    AWS_SECRET_ACCESS_KEY = config.get('AWS', 'SECRET')

    #creates bucket that points to data
    s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket('deutsche-boerse-xetra-pds')

    #the deutsche-boerse-xetra-pds bucket contains a list of csv links that
    #point to data for each hour of trading
    #first, iterate through each object (link to csv) in the bucket
    for object in bucket.objects.all():

            #filter for non-trading hours (empty csv) by size
            #files with size 136 bytes indicate off hours logging and
            #should be ommitted
        if object.size > 136:
            url = 'https://s3.eu-central-1.amazonaws.com/deutsche-boerse-xetra-pds/' + object.key

            data = pd.read_csv(url)

            #read through each line of csv and send the line to the kafka topic
            #files with size 136 bytes indicate off hours logging and
            #should be ommitted
            for index, row in data.iterrows():
                output = ''
                for element in row:
                    output = output + str(element) + "^"

                producer.send(topic='stockdataset', value=output.encode())
                producer.flush()
        #producer.close()
    return

if __name__ == '__main__':
        main()
