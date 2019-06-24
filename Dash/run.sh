#!/bin/bash

ssh ubuntu@10.0.0.8 '/usr/local/spark/bin/spark-submit --master spark://10.0.0.8:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.2.0 --jars /usr/local/spark/jars/postgresql-42.2.4.jar preprocessing.py'
ssh ubuntu@10.0.0.11 'python producer.py'
