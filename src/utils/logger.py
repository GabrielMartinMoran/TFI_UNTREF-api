import os
import logging
import re
from logging.handlers import TimedRotatingFileHandler
import src.config as config

SRC_FOLDER = 'src'


class Logger:
    __instance__ = None

    def __init__(self):
        if Logger.__instance__ is None:
            Logger.__create_path()
            Logger.__instance__ = logging.getLogger("App")
            Logger.__instance__.setLevel(config.LOG_LEVEL)  # lowest level
            Logger.__instance__.addHandler(Logger.__get_file_handler())
        else:
            raise Exception("Logger es un singleton!")

    @staticmethod
    def __get_file_handler():
        file_handler = TimedRotatingFileHandler(
            os.path.join(config.LOGS_FOLDER, config.LOG_FILE_NAME),
            when=config.ROTATION_FREQUENCY, interval=config.ROTATION_INTERVAL,
            backupCount=config.BACKUP_COUNT, delay=0)
        file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
        file_handler.suffix = config.ROTATION_SUFFIX
        file_handler.extMatch = re.compile(config.ROTATION_SUFFIX_REGEX)
        return file_handler

    @staticmethod
    def get_logger(name: str):
        if Logger.__instance__ is None:
            Logger()
        Logger.__instance__.name = name.split('src')[1]
        return Logger.__instance__

    @staticmethod
    def __create_path():
        path = os.path.join(config.LOGS_FOLDER, config.LOG_FILE_NAME)
        # Creamos el directorio
        if not os.path.exists(config.LOGS_FOLDER):
            os.mkdir(config.LOGS_FOLDER)
        # Creamos el archivo
        if not os.path.exists(path):
            f = open(path, 'w')
            f.close()
