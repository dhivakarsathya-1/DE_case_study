from pyspark.sql import SparkSession
from src.common.config import Config

class Utils:

    @classmethod
    def get_spark(cls):
        cls.spark_session = SparkSession.builder\
            .appName(Config.APP_NAME)\
            .master("local[*]")\
            .config("spark.driver.bindAddress", "127.0.0.1")\
            .config("spark.driver.host", "localhost")\
            .config("spark.jars.packages", Config.KAFKA_PACKAGE)\
            .getOrCreate()

        return cls.spark_session