"""Configuration file for logging to be reused across all modules and scripts"""
import logging


logging.basicConfig(filename='debug.log', # filename in which info are logged
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s')

def get_logger():
    """Enables export of the logger config to be used across modules"""
    return logging.getLogger(__name__)