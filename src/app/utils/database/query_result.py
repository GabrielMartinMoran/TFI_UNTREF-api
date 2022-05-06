from typing import List, Type, Optional

from psycopg2 import extensions

from src.domain.models import BaseModel


class QueryResult:

    def __init__(self) -> None:
        self.columns = []
        self.rows = []
        self.records = []
        self.rows_affected = 0

    def from_cursor(self, cursor: extensions.cursor) -> None:
        self.rows_affected = cursor.rowcount
        # Si no tiene columnas significa que no devolvio nada la query
        if not cursor.description:
            return
        self.columns = [x.name for x in cursor.description]
        self.rows = cursor.fetchall()
        self.records = []
        for row in self.rows:
            record = {}
            for i, col in enumerate(self.columns):
                record[col] = row[i]
            self.records.append(record)

    def first(self) -> dict:
        if not self.records:
            return {}
        return self.records[0]

    def map_first(self, model_class: Type[BaseModel]) -> Optional[BaseModel]:
        if not self.records:
            return None
        return model_class.from_dict(self.records[0])

    def map_all(self, model_class: Type[BaseModel]) -> List[BaseModel]:
        return [model_class.from_dict(x) for x in self.records]
