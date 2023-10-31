import pytest

from src import config
from src.infrastructure.database.db_migrator import DBMigrator

# Import steps for autoload
from tests.integration.steps.user_register_steps import *  # noqa: F401, F403
from tests.integration.steps.user_login_steps import *  # noqa: F401, F403
from tests.integration.steps.device_steps import *  # noqa: F401, F403
from tests.integration.steps.user_data_steps import *  # noqa: F401, F403
from tests.integration.steps.device_scheduler_steps import *  # noqa: F401, F403
from tests.integration.steps.device_token_steps import *  # noqa: F401, F403

migrator = None
DROP_DB = True


def setup_database():
    global migrator
    print('Setting up testing database')
    config.DB_NAME = 'devices_management_test'
    # DB_USERNAME and DB_PASSWORD must be set as env var if they differ
    if config.DB_USERNAME is None:
        config.DB_USERNAME = 'postgres'
    if config.DB_PASSWORD is None:
        config.DB_PASSWORD = 'postgres'
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
