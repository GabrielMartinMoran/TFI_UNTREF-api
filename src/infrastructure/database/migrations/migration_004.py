from src.infrastructure.database.migrations.base_migration import BaseMigration


class Migration004(BaseMigration):
    MIGRATION_NUMBER = 4

    def apply_migration(self, cursor):
        # Drop colum active from Devices
        queries = [
            "ALTER TABLE Devices DROP COLUMN active"
        ]
        self._execute_sql(queries, cursor)
