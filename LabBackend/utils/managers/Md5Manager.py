import hashlib
import random
import uuid
from datetime import datetime
from LabBackend.utils.Interfaces import IIdentifiable


class Md5Manager(IIdentifiable):
    def __init__(self):
        self.rand = random.Random()

    def generate_id(self) -> str:
        current_time = datetime.utcnow()
        random_value = self.rand.random()
        unique_data = f"{current_time.timestamp()}{random_value}{uuid.uuid4()}"

        md5_hash = hashlib.md5(unique_data.encode('utf-8')).hexdigest()
        return md5_hash