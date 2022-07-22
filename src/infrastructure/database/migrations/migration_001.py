from src.infrastructure.database.migrations.base_migration import BaseMigration


class Migration001(BaseMigration):
    MIGRATION_NUMBER = 1

    def apply_migration(self, cursor):
        queries = [
            "CREATE TABLE Users (user_id VARCHAR NOT NULL PRIMARY KEY, username VARCHAR NOT NULL, "
            "email VARCHAR NOT NULL, hashed_password VARCHAR NOT NULL, created_date TIMESTAMP NOT NULL DEFAULT NOW())",

            "CREATE TABLE Devices (device_id VARCHAR NOT NULL PRIMARY KEY, user_id VARCHAR NOT NULL, "
            "name character varying NOT NULL, active boolean NOT NULL, "
            "turned_on boolean NOT NULL, created_date TIMESTAMP NOT NULL DEFAULT NOW(), "
            "CONSTRAINT devices_users_fk FOREIGN KEY (user_id) REFERENCES users (user_id) MATCH SIMPLE ON UPDATE "
            "NO ACTION ON DELETE CASCADE NOT VALID)",

            "CREATE TABLE Measures (measure_id serial NOT NULL PRIMARY KEY, device_id VARCHAR NOT NULL, "
            "voltage numeric NOT NULL, current numeric NOT NULL, \"timestamp\" TIMESTAMP NOT NULL, "
            "CONSTRAINT measures_devices_fk FOREIGN KEY (device_id) REFERENCES devices (device_id) MATCH SIMPLE ON "
            "UPDATE NO ACTION ON DELETE CASCADE NOT VALID)",

            "CREATE TABLE DeviceTasks (device_id VARCHAR NOT NULL, tasks JSONB NOT NULL, "
            "CONSTRAINT devicetasks_devices_fk FOREIGN KEY (device_id) REFERENCES devices (device_id) MATCH SIMPLE ON "
            "UPDATE NO ACTION ON DELETE CASCADE NOT VALID)",
        ]
        self._execute_sql(queries, cursor)
