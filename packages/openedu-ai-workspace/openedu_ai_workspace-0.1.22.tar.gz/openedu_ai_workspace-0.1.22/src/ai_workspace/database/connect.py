from urllib.parse import urlparse

from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)

        # Lấy db_name từ MongoDB URI
        parsed_uri = urlparse(uri)
        db_name = parsed_uri.path.lstrip("/")  # Lấy tên DB từ URI

        self.db = self.client[db_name]

    def close(self):
        self.client.close()
