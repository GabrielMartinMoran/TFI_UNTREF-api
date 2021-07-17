from copy import deepcopy
import types
from typing import List


class QueryResult:

    def __init__(self) -> None:
        self.colums = []
        self.rows = []
        self.table = {}
        self.rows_affected = 0

    def from_cursor(self, cursor: object) -> None:
        self.rows_affected = cursor.rowcount
        # Si no tiene columnas significa que no devolvio nada la query
        if not cursor.description:
            return
        self.colums = [x.name for x in cursor.description]
        self.rows = cursor.fetchall()
        self.table = {}
        for col in self.colums:
            self.table[col] = []
        for row in self.rows:
            for i, col in enumerate(self.colums):
                self.table[col].append(row[i])

    def first_to_model(self, model_instance_example: object) -> object:
        models = self.to_model_list(model_instance_example)
        if len(models) > 0:
            return models[0]
        return None

    def to_model_list(self, model_instance_example: object) -> List[object]:
        attributes = self.__get_object_attributes(model_instance_example)
        result = []
        for row in self.rows:
            model = deepcopy(model_instance_example)
            for i, col in enumerate(self.colums):
                if col in attributes:
                    setattr(model, col, row[i])
            result.append(model)
        return result

    def __get_object_attributes(self, model_instance: object):
        return [ x for x in dir(model_instance) if 
                    type(getattr(model_instance, x)) != types.MethodType and
                    not x.startswith('__')
        ]