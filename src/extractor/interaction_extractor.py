from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.sql.functions import col, from_json
from loguru import logger

class InteractionExtractor:

    """
    Extracts Interaction streaming data from Kafka topics
    """

    logger.info(f"Inside Extractor")

    def __init__(self, spark, topic_name, offset, bootstrap_servers):
        self.spark = spark
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers
        self.offset = offset

    def read_from_kafka(self):
        custom_schema = StructType([
            StructField("user_id", StringType()),
            StructField ("item_id", StringType()),
            StructField("interaction_type", StringType()),
            StructField("timestamp", TimestampType())
        ])

        raw_df = self.spark.readStream.format("kafka")\
                .option("kafka.bootstrap.servers", self.bootstrap_servers)\
                .option("subscribe", self.topic_name) \
                .option("startingOffsets", self.offset)\
                .load()

        raw_df_final = raw_df.selectExpr("CAST(value as STRING)")\
                        .select(from_json(col("value"), schema=custom_schema).alias("raw_data"))\
                        .select("raw_data.*")

        logger.info(f"Successfully created stream from topic: {self.topic_name}")

        return raw_df_final