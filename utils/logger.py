import logging
import os
import sys

from utils.tools import abspath


def create_logger(name="main", level=logging.INFO) -> logging.Logger:
    if "logs" not in os.listdir(sys.argv[1]): os.mkdir(abspath("logs"))
    format = '%(asctime)-15s: %(levelname)s %(message)s'
    logger = logging.getLogger()
    logger.setLevel(level)
    fh = logging.FileHandler(abspath(f'logs/{name}_logs.log'))
    fh.setLevel(level)
    formatter = logging.Formatter(format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
