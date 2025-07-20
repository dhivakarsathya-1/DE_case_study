import os
from loguru import logger
from pyspark.sql import DataFrame

class InteractionLoader:

    logger.info(f"Inside Loader")

    def __init__(self, destination_path, checkpoint_location):
        self.destination_path = destination_path
        self.checkpoint_location = checkpoint_location

        #check directories else create
        # ( since running in Local machine I am creating,
        # if in lakehouse/delta lake we can configure to the specific storage account / bucket)
        directories = [
            f"{self.destination_path}/raw_interactions",
            f"{self.destination_path}/user_aggregations",
            f"{self.destination_path}/item_aggregations",
            self.checkpoint_location
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def write(self, final_transformed:dict):
        batch_id = final_transformed["batch_id"]
        logger.info(f"Starting write for batch {batch_id}")

        raw_df = final_transformed["raw_interactions"]
        user_agg_df = final_transformed["user_agg"]
        item_agg_df = final_transformed["item_agg"]

        raw_df.write.mode("append").partitionBy("partition_by_column")\
            .parquet(f"{self.destination_path}/raw_interactions")
        user_agg_df.write.mode("append").partitionBy("partition_by_column")\
            .parquet(f"{self.destination_path}/user_aggregations")
        item_agg_df.write.mode("append").partitionBy("partition_by_column")\
            .parquet(f"{self.destination_path}/item_aggregations")

        logger.info(f"Starting write for batch {batch_id}")


    def stream_write(self, stream_df:DataFrame, transform_function, trigger_interval):
        def write_batch(df, batch_id):
            if df.count() > 0:
                result = transform_function(df, batch_id)
                self.write(result)

        final_write = stream_df.writeStream.foreachBatch(write_batch)\
                        .option("checkpointLocation", self.checkpoint_location)\
                        .trigger(processingTime=trigger_interval) \
                        .start()

        return final_write
