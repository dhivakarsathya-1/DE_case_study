class Config:

    # Kafka settings
    BOOTSTRAP_SERVERS = "127.0.0.1:9092"
    TOPIC_NAME = "interactions"
    OFFSET="latest"


    # Spark settings
    APP_NAME = "InteractionDemo"
    KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"

    # File paths
    DESTINATION_PATH = "./output"
    CHECKPOINT_LOCATION = "./checkpoints"

    # Streaming settings
    TRIGGER_INTERVAL = "10 seconds"