from kafka import KafkaProducer
from src.data_gen.generator import DataGenerator
import json
import time
from loguru import logger

class KafkaProducerClient:

    def __init__(self, delay, topic, bootstrap_servers):
        self.delay = delay # introducing delay variable to control the rate of data generation
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers = bootstrap_servers,
            value_serializer = lambda x: json.dumps(x).encode('utf-8')

        )
        self.data = DataGenerator()

    def publish_messages(self, count):
        logger.info(f"Inside Publish Message to Kafka")
        for i in range(count):
            message = self.data.generate_data()
            self.producer.send(topic=self.topic, value=message)
            time.sleep(self.delay)
        self.producer.flush()
        logger.info(f"Published {count} messages")