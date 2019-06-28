from pyspark.sql import DataFrameWriter
import os

class PostgreSQLConnect(object):
    """
    Provide connection parameters for PostgreSQL connection
    """
    def __init__(self):
        self.database_name = 'DB_NAME'
        self.hostname = 'HOST_NAME'
        self.url_connect = "jdbc:postgresql://{hostname}:5432/{db}"
                            .format(hostname=self.hostname, db=self.database_name)
        self.properties = {"user":"DB_USER",
                           "password" : "DB_PASSWORD",
                           "driver": "org.postgresql.Driver"
                           }

    def get_writer(self, df):
        return DataFrameWriter(df)

    def write(self, df, table, md):
        my_writer = self.get_writer(df)
        df.write.jdbc(url=self.url_connect, table=table, mode=md, properties=self.properties)
