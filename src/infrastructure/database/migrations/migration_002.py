from src.infrastructure.database.migrations.base_migration import BaseMigration


class Migration002(BaseMigration):
    MIGRATION_NUMBER = 2

    def apply_migration(self, cursor):
        queries = [
            "ALTER TABLE Devices ADD COLUMN last_status_update TIMESTAMP",
        ]
        self._execute_sql(queries, cursor)
