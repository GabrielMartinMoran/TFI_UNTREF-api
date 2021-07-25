import src.config as config
import psycopg2
from src.app.utils.database.query_result import QueryResult


class PostgresRepository:

    def _execute_query(self, query: str, transaction=None) -> QueryResult:
        conn = transaction
        if not conn:
            conn = self._create_transaction()
        cursor = conn.cursor()
        result = QueryResult()
        try:
            cursor.execute(query)
            result.from_cursor(cursor)
            cursor.close()
            if not transaction:
                conn.commit()
        except Exception as e:
            if not transaction:
                conn.rollback()
            raise Exception(e)
        finally:
            if not transaction:
                conn.close()
        return result

    def _create_transaction(self):
        conn_string = f"user='{config.DB_USERNAME}' password='{config.DB_PASSWORD}' host='{config.DB_URL}' " \
                      f"port='{config.DB_PORT}' dbname='{config.DB_NAME}'"
        return psycopg2.connect(conn_string)
