from src.infrastructure.database.migrations.base_migration import BaseMigration


class Migration003(BaseMigration):
    MIGRATION_NUMBER = 3

    def apply_migration(self, cursor):
        queries = [
            "CREATE TABLE InstantActions (device_id VARCHAR NOT NULL, action VARCHAR NOT NULL NOT NULL, "
            "\"timestamp\" TIMESTAMP NOT NULL, "
            "CONSTRAINT instantactions_devices_fk FOREIGN KEY (device_id) REFERENCES devices (device_id) MATCH SIMPLE "
            "ON UPDATE NO ACTION ON DELETE CASCADE NOT VALID)",
        ]
        self._execute_sql(queries, cursor)
