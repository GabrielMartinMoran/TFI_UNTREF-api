import os

"""
Variables de entorno:
- DB_PORT
- DB_URL
- APP_SECRET
"""

# --------------------- #
# -        APP        - #
# --------------------- #
APP_PORT = 5000
APP_USE_RELOADER = False
APP_RUN_DEBUG_MODE = True
CLIENT_APP_FOLDER = './client'
HOST = '0.0.0.0'  # For running it locally but exposed

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

# Reemplazar el {0} por el MD5 del email
GRAVATAR_AUTOGENERATED_AVATAR_URL = 'https://www.gravatar.com/avatar/{0}?d=identicon&r=PG&s=500'

# --------------------- #
# -        LOG        - #
# --------------------- #
LOG_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
LOGS_FOLDER = './logs'
LOG_FILE_NAME = 'logfile.log'
LOG_LEVEL = 10  # logging DEBUG
BACKUP_COUNT = 20
ROTATION_FREQUENCY = 'H'  # 'H' 'D' 'midnight' entre otros...
ROTATION_INTERVAL = 1
ROTATION_SUFFIX = '%Y-%m-%d_%H_%M_%S.log'
ROTATION_SUFFIX_REGEX = r'^\d{4}-\d{2}-\d{2}_-\d{2}-\d{2}-\d{2}.log$'


# --------------------- #
# -    ERROR CODES    - #
# --------------------- #
class ErrorCodes:
    ACCOUNT_NOT_VERIFIED = 'ACCOUNT_NOT_VERIFIED'


# --------------------- #
# -MEASURES SUMMARIZER- #
# --------------------- #
MAX_SUMMARIZED_MEASURES_TO_SHOW = 25

# --------------------- #
# -  INSTANT ACTIONS  - #
# --------------------- #
INSTANT_ACTIONS_LIFETIME = 20  # Seconds
