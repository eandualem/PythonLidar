import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from config import Config

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def get_console_handler():
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setFormatter(FORMATTER)
  return console_handler


def get_file_handler():
  file_handler = TimedRotatingFileHandler(Config.LOG_FILE, when='midnight')
  file_handler.setFormatter(FORMATTER)
  return file_handler


def get_logger(logger_name):
  logger = logging.getLogger(logger_name)
  # better to have too much log than not enough
  logger.setLevel(logging.DEBUG)
  logger.addHandler(get_console_handler())
  logger.addHandler(get_file_handler())
  # with this pattern, it's rarely necessary to propagate the error up to parent
  logger.propagate = False
  return logger
