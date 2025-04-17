import abc
from pymongo.synchronous.database import Database


class MongoService:
    db: Database

    def __init__(self, db: Database) -> None:
        self.db = db

    @abc.abstractmethod
    def build_index(self, **kwargs):
        pass

    @abc.abstractmethod
    def create_collections(self, **kwargs):
        pass
