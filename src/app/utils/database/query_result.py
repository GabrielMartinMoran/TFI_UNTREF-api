from typing import List, Type, Optional, Any

from psycopg2 import extensions

from src.domain.mappers.mapper import Mapper


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

    def map_first(self, mapper: Type[Mapper]) -> Optional[Any]:
        if not self.records:
            return None
        return mapper.map(self.records[0])

    def map_all(self, mapper: Type[Mapper]) -> List[Any]:
        return mapper.map_all(self.records)
