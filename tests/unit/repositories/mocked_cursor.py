from typing import List


class CursorColumnDescription():

    def __init__(self, name) -> None:
        self.name = name

class MockedCursor():

    def __init__(self) -> None:
        self.execute_raises_exception = False
        self.executed_query = ''
        self.rowcount = 0
        self.description = None
        self.rows = []

    def prepare(self, table: dict = {}, affected_rows: int=0, execute_raises_exception=False) -> None:
        self.execute_raises_exception = execute_raises_exception
        self.executed_query = ''
        self.rowcount = affected_rows
        self.description = [CursorColumnDescription(x) for x in table] if len(table) > 0 else None
        self.rows = []
        if not self.description or len(self.description) == 0:
            return
        rows_count = len(table[self.description[0].name])
        for i in range(rows_count):
            row = []
            for col in self.description:
                row.append(table[col.name][i])
            self.rows.append(row)

    def execute(self, query):
        self.executed_query = query
        if self.execute_raises_exception:
            raise Exception('Mocked exception')

    def close(self):
        pass

    def fetchall(self) -> List[List[object]]:
        return self.rows