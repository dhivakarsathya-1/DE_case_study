from src.data_gen.producer import KafkaProducerClient
from src.common.config import Config
from src.common.utils import Utils
from loguru import logger
import argparse
from src.extractor.interaction_extractor import InteractionExtractor
from src.transformer.interaction_transformer import InteractionTransformer
from src.loader.interaction_loader import InteractionLoader

def run_producer(message_count, time_delay):

    try:
        producer = KafkaProducerClient(topic=Config.TOPIC_NAME, delay=time_delay, bootstrap_servers=Config.BOOTSTRAP_SERVERS)
        producer.publish_messages(count=message_count)
    except Exception as e:
        logger.info(f"Producer failed with {e}")

def run_consumer():

    try:
        extract = InteractionExtractor(Utils.get_spark(), Config.TOPIC_NAME, Config.OFFSET, Config.BOOTSTRAP_SERVERS)
        loader = InteractionLoader(Config.DESTINATION_PATH, Config.CHECKPOINT_LOCATION)

        logger.info("Starting streaming...")
        stream_df = extract.read_from_kafka()
        query = loader.stream_write(stream_df, InteractionTransformer.transform, Config.TRIGGER_INTERVAL)

        logger.info("Pipeline started! Press Ctrl+C to stop")
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Stopping...")
    finally:
        Utils.get_spark().stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['producer', 'consumer'], required=True)
    parser.add_argument('--count', type=int, default=None)
    parser.add_argument('--delay', type=int)

    args = parser.parse_args()

    if args.mode == 'producer':
        # command to run producer ->  python -m runner --mode producer --count 10 --delay 1
        run_producer(message_count=args.count, time_delay=args.delay)
    elif args.mode == 'consumer':
        # command to run consumer -> python -m runner --mode consumer
        run_consumer()
