import os
import sys
from multiprocessing import Process, freeze_support
from typing import TYPE_CHECKING

from models.configuration import load_configuration
from models.models_file import AppConfiguration
from server import Server
from utils.logger import create_logger

import pkg_resources.py2_warn

if TYPE_CHECKING:
    from typing import List



def get_servers(config) -> 'List[Server]':
    environments = load_configuration(config.mockoon_file)
    servers = [Server.factory(config.host, environment, debug=config.flask_debug, logging_level=config.logging_level)
               for environment in environments]

    return servers


def main():
    config = AppConfiguration.fromFile("config.yaml")
    logger = create_logger(level=config.logging_level)
    try:
        servers = get_servers(config)
    except Exception as e:
        logger.error("Error in get_servers(): %s", e)
        raise SystemExit
    processes = [Process(target=server.run) for server in servers]
    yield processes
    [proc.start() for proc in processes]
    [proc.join() for proc in processes]
    yield None


if __name__ == '__main__':
    freeze_support()
    sequence = main()
    processes = next(sequence)
    start = next(sequence)
