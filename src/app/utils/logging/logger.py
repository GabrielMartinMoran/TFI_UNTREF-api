from loguru import logger


class Logger:

    @staticmethod
    def debug(message: str):
        logger.debug(message)

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def error(exception: Exception):
        logger.error(repr(exception))
