import logging

def create_logger(name="main"):
    FORMAT = '%(asctime)-15s: %(levelname)s  %(message)s'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f'logs/{name}_logs.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    fh.setFormatter(formatter)
    logger.addHandler(fh)



