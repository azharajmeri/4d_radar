import logging


def get_logger():
    logger = logging.getLogger('speed_logs')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('speed_logs.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger
