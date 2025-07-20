from faker import Faker
from loguru import logger
import random
import datetime

class DataGenerator:

    def __init__(self, num_users=10, num_items=10):
        self.fake = Faker()
        self.interaction_types = ['click', 'view', 'purchase']

        # Create a fixed pool of users and items
        self.user_ids = [self.fake.uuid4() for _ in range(num_users)]
        self.item_ids = list(range(1, num_items + 1))

    def generate_data(self):
        logger.info("Inside data generator")
        return {
            "user_id": random.choice(self.user_ids),
            "item_id": random.choice(self.item_ids),
            "interaction_type": random.choice(self.interaction_types),
            "timestamp": datetime.datetime.now().isoformat()
        }