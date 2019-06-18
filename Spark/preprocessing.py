from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SQLContext
#import psycopg2

def main():
    #Create spark job and name it
    sc = SparkContext(appName = 'updated_testjob')
    #Prevent spark from displaying all logs messages
    sc.setLogLevel('Error')
    #Provides methods used to create Dstreams from various input source
    #Note: metadata.broker.list might be depreciated and need to be replaced
    #with bootstrap.servers
    ssc = StreamingContext(sc, 1)
    #parse the row into separate components
    kafkaStream = KafkaUtils.createDirectStream(ssc,
                    ['rawDBGData'], {'metadata.broker.list':
                    'ec2-50-112-13-159.us-west-2.compute.amazonaws.com:9092'})
    #parse the row into separate components
    filteredStream = kafkaStream.map(lambda line: line[1].split("^"))
    print(filteredStream)
    return
if __name__ == '__main__':
        main()
