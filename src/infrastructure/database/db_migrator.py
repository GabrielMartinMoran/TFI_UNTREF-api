import sys
import os
from src.app.utils import console_colors
from src import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.common import dates
from src.infrastructure.database.migrations.migration_001 import Migration001
from src.infrastructure.database.migrations.migration_002 import Migration002
from src.infrastructure.database.migrations.migration_003 import Migration003
from src.infrastructure.database.migrations.migration_004 import Migration004


class DBMigrator:
    MIGRATIONS = [
        Migration001,
        Migration002,
        Migration003,
        Migration004,
    ]

    def __init__(self):
        self.app_info = None
        self.create_db_if_not_exists()
        self.load_app_info()

    def create_db_if_not_exists(self):
        db_exists = True
        conn = self.__get_db_connection(specify_database=False)
        # Porque no es posible crear la base en transaccion
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT COUNT(DATNAME) FROM PG_CATALOG.PG_DATABASE WHERE LOWER(DATNAME) = LOWER('{config.DB_NAME}')")
            db_exists = cursor.fetchone()[0] > 0
            if not db_exists:
                cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()
        if not db_exists:
            self.__create_app_info()

    # Solo para testing
    def drop_db(self):
        conn = self.__get_db_connection(specify_database=False)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        try:
            cursor.execute(f"DROP DATABASE {config.DB_NAME}")
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()

    def __get_db_connection(self, specify_database=True):
        conn_string = f"user='{config.DB_USERNAME}' password='{config.DB_PASSWORD}' host='{config.DB_URL}' " \
                      f"port='{config.DB_PORT}'"
        if specify_database:
            conn_string += f" dbname='{config.DB_NAME}'"
        return psycopg2.connect(conn_string)

    def __create_app_info(self):
        conn = self.__get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE AppInfo (key VARCHAR(255) PRIMARY KEY, value VARCHAR(255) NOT NULL)")
            cursor.execute(
                f"INSERT INTO AppInfo (key, value) VALUES ('{config.LAST_MIGRATION_APP_INFO_KEY}', 0), "
                f"('{config.LAST_MIGRATION_APP_INFO_DATE}', NOW())")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            conn.close()

    def run_migrations(self):
        print(F'{console_colors.INFO}Corriendo migraciones de la base de datos:{console_colors.ENDC}')
        self.MIGRATIONS.sort(key=lambda x: x.MIGRATION_NUMBER)
        # Todas las migraciones se ejecutan en una sola transaccion
        conn = self.__get_db_connection()
        cursor = conn.cursor()
        for x in self.MIGRATIONS:
            common_msg = F'la migracion {x.MIGRATION_NUMBER} del archivo {self.get_migration_filename(x)}' \
                         F'{console_colors.ENDC}'
            if x.MIGRATION_NUMBER <= self.get_last_applied_migration():
                print(F'{console_colors.WARNING} ‣ Saltando {common_msg}')
            else:
                print(F'{console_colors.OK} ‣ Aplicando {common_msg}')
                try:
                    self.__apply_migration(x, cursor)
                except Exception as e:
                    conn.rollback()
                    conn.close()
                    raise Exception(e)
        conn.commit()
        conn.close()
        print('\n\n')

    def load_app_info(self):
        conn = self.__get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM AppInfo")
            self.app_info = {}
            for key, value in cursor.fetchall():
                self.app_info[key] = value
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()

    def get_last_applied_migration(self):
        if self.app_info:
            return int(self.app_info[config.LAST_MIGRATION_APP_INFO_KEY])
        return 0

    def __apply_migration(self, migration_class: type, cursor: object):
        migration_class().apply_migration(cursor)
        self.update_to_last_migration(migration_class.MIGRATION_NUMBER, cursor)

    def update_to_last_migration(self, last_migration_number: int, cursor: object):
        cursor.execute(f"UPDATE AppInfo SET value = '{last_migration_number}' WHERE "
                       f"key = '{config.LAST_MIGRATION_APP_INFO_KEY}'")
        cursor.execute(f"UPDATE AppInfo SET value = '{dates.now()}' WHERE "
                       f"key = '{config.LAST_MIGRATION_APP_INFO_DATE}'")

    def get_migration_filename(self, migration_class):
        return os.path.split(sys.modules[migration_class.__module__].__file__)[1]
