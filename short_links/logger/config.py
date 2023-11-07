"""Config for logging"""
import logging
import os

from common.settings import logging_path


logging.basicConfig(
    filename=logging_path + os.sep + 'log.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s',
    level=logging.INFO
)
