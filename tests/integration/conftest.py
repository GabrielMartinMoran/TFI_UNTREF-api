import pytest
from src.database.db_migrator import DBMigrator, config

migrator = None
DROP_DB = True


def setup_database():
    global migrator
    print('Setting up testing database')
    config.DB_NAME = 'devices_management_test'
    # DB_USERNAME and DB_PASSWORD must be set as env var
    migrator = DBMigrator()
    migrator.run_migrations()


def clean_database():
    global migrator
    print('Cleaning testing database')
    if DROP_DB:
        migrator.drop_db()


@pytest.fixture(scope="session", autouse=True)
def configure_tests_env(*args, **kwargs):
    setup_database()
    yield  # Yield to run all tests
    clean_database()
