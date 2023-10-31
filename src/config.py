import os

# --------------------- #
# -        APP        - #
# --------------------- #
APP_PORT = 5000
APP_USE_RELOADER = False
APP_RUN_DEBUG_MODE = True
CLIENT_APP_FOLDER = './client'
HOST = '0.0.0.0'  # For running it locally, but exposed to the LAN

# --------------------- #
# -     APP INFO      - #
# --------------------- #
APP_INFO_COLLECTION = 'app'
LAST_MIGRATION_APP_INFO_KEY = 'last_migration'
LAST_MIGRATION_APP_INFO_DATE = 'last_migration_date'

# --------------------- #
# -      DATABASE     - #
# --------------------- #
DB_URL = os.environ.get('DB_URL', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'devices_management_dev')
DB_USERNAME = os.environ.get('DB_USERNAME', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

# --------------------- #
# -        JWT        - #
# --------------------- #
APP_SECRET = os.environ.get('APP_SECRET', 'WeapAppSecret')
HASH_ALGORITHM = 'HS256'

# --------------------- #
# -MEASURES SUMMARIZER- #
# --------------------- #
MAX_SUMMARIZED_MEASURES_TO_SHOW = 25

# --------------------- #
# -  INSTANT ACTIONS  - #
# --------------------- #
INSTANT_ACTIONS_LIFETIME = 20  # Seconds
