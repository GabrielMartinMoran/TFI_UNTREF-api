from re import I
from typing import List
from pymongo import MongoClient
from src import config


class BaseMigration:

    MIGRATION_NUMBER = None

    def __init__(self) -> None:
        pass

    def apply_migration(self, cursor: object):
        pass

    def _execute_sql(self, queries: List[str], cursor: object):
        for query in queries:
            cursor.execute(query)