import os
import logging
from datetime import datetime


def get_logger():
    # Get current date each time the function is called
    current_date = datetime.now().strftime('%Y%m%d')

    # Create folder if it doesn't exist
    log_folder = os.path.join('logs', current_date)
    os.makedirs(log_folder, exist_ok=True)

    # Set up logger
    logger = logging.getLogger('speed_logs')
    logger.setLevel(logging.DEBUG)

    # Create file handler which logs even debug messages
    log_file = os.path.join(log_folder, 'speed_logs.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(fh)

    return logger
