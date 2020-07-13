import logging


def create_logger(name="main", level = "DEBUG") -> logging.Logger:
    FORMAT = '%(asctime)-15s: %(levelname)s %(message)s'
    logger = logging.getLogger()
    logger.setLevel(level)
    fh = logging.FileHandler(f'logs/{name}_logs.log')
    fh.setLevel(level)
    formatter = logging.Formatter(FORMAT)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
