import sys
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler


class ShLogger:
    FORMATTER = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
    """ Class represent logging handlers"""
    def __init__(self, logger_name: str, frmt: logging.Formatter, logger_level=logging.DEBUG, propagate: bool = False):
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logger_level)
        self.formatter = frmt
        self.set_propagate(propagate=propagate)

    def add_console_handler(self, level=logging.DEBUG):
        """
        Function return handler to send info in STDOUT
        :param level: set logging level
        """
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        handler.setLevel(level)
        return self.logger.addHandler(handler)

    def add_file_handler(self, log_filename: str = None, level=logging.INFO):
        """
        Function return handler to send info in FILE
        :param str log_filename: filename to save log message
        :param level: set logging level
        """
        if log_filename is None:
            log_filename = self.logger_name

        handler = TimedRotatingFileHandler(filename=log_filename, encoding="utf-8", when='midnight', backupCount=3)
        handler.setFormatter(self.formatter)
        handler.setLevel(level)
        return self.logger.addHandler(handler)

    def set_propagate(self, propagate: bool):
        self.logger.propagate = propagate

    def critical(self, msg):
        self.logger.info(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)

    def warning(self, msg):
        self.logger.warning(msg=msg)

    def info(self, msg):
        self.logger.info(msg=msg)

    def debug(self, msg):
        self.logger.debug(msg=msg)

    def exception(self, msg):
        self.logger.exception(msg=msg)
