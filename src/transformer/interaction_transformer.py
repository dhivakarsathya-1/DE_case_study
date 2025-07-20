from pyspark.sql import DataFrame
from pyspark.sql.functions import col,count,lit, max as sp_max, min as sp_min,date_format
from loguru import logger

class InteractionTransformer:

    logger.info(f"Inside Transformer")

    def transform(raw_df:DataFrame, batch_id):
        """
        Transforms interaction raw data and performs real-time aggregations
        """

        # DQ check
        cleaned_df = raw_df.filter(
            col("user_id").isNotNull() &
            col("item_id").isNotNull() &
            col("interaction_type").isNotNull() &
            col("timestamp").isNotNull()
        ).withColumn("batch_id", lit(batch_id))\
        .withColumn("partition_by_column", date_format(col("timestamp"), "yyyy-MM-dd-HH"))

        # User Aggregations
        user_interaction_df = cleaned_df.groupBy(col("user_id"), col("partition_by_column")).agg(
            count(col("interaction_type")).alias("total_user_interactions"),
            sp_max(col("timestamp")).alias("last_interaction")
        )

        # Maximum and minimum interactions per item.
        item_interaction_df = cleaned_df.groupBy(col("item_id"), col("partition_by_column")).agg(
            count(col("interaction_type")).alias("total_item_interactions"),
            sp_min(col("timestamp")).alias("min_interaction_time"),
            sp_max(col("timestamp")).alias("max_interaction_time")
        )

        final_transformed = {
            "raw_interactions" : cleaned_df,
            "user_agg": user_interaction_df,
            "item_agg": item_interaction_df,
            "batch_id": batch_id
        }

        logger.info(f"Transformation completed for batch {batch_id}")

        return final_transformed