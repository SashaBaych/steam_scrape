import logging
import datetime
import os

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
LOG_FILE_NAME = f"st_log_{TIMESTAMP}.log"


def get_logger(file):
    """
    Returns a logger object with a file handler and a stream handler configured.

    Parameters:
        file (str): The path to the file where the logger is being configured.

    Returns:
        logging.Logger: A logger object that can be used to write log messages to a file and/or the console.
    """
    logging.basicConfig(format='%(name)s; %(levelname)s; %(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(LOG_FILE_NAME),
                            logging.StreamHandler()
                        ])
    return logging.getLogger(os.path.basename(file))


def logger_decorator(func):
    """
    A decorator function that wraps a given function and adds error logging functionality.

    Parameters:
        func (callable): The function to be wrapped by the decorator.

    Returns:
        callable: A wrapper function that calls the original function and logs any errors that occur.
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__file__)
        logger.info(f"Starting {func.__name__} function...")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} function executed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper
