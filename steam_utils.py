import logging
import datetime
import os

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
LOG_FILE_NAME = f"st_log_{TIMESTAMP}.log"


def get_logger(file):
    logging.basicConfig(format='%(name)s; %(levelname)s; %(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(LOG_FILE_NAME),
                            logging.StreamHandler()
                        ])
    return logging.getLogger(os.path.basename(file))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__file__)
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper
