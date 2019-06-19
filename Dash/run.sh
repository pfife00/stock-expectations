#!/bin/bash

#ssh ubuntu@ec2-34-209-70-4.us-west-2.compute.amazonaws.com '/usr/local/spark/bin/spark-submit --master local[4] SimpleApp.py'
#ssh ubuntu@ec2-34-209-70-4.us-west-2.compute.amazonaws.com /usr/local/spark/bin spark-submit --master spark://ec2-34-209-70-4.us-west-2.compute.amazonaws.com:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 'preprocessing.py'
ssh ubuntu@10.0.0.9 'python producer.py'

ssh ubuntu@10.0.0.7  spark-submit --master spark://10.0.0.7:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 'preprocessing.py'

#ssh ubuntu@ec2-50-112-13-159.us-west-2.compute.amazonaws.com 'python producer.py'
#ssh ubuntu@KAFKA_IP_ADDRESS 'python producer.py'
