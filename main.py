import logging
import os
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING

from models.configuration import Configuration
from models.logger import create_logger
from server import Server

if TYPE_CHECKING:
    from typing import List

if "logs" not in os.listdir(): os.mkdir("logs")

HOST = "0.0.0.0"
DEBUG = False
CONFIGURATION_FILE = 'mockoon_configuration.json'


def main() -> 'List[Server]':
    create_logger()

    configuration = Configuration(f"mockoon_files/{CONFIGURATION_FILE}")
    environments = configuration.load_configuration()
    servers = [Server.factory(HOST, environment) for environment in environments]

    return servers


def run(servers: 'List[Server]') -> None:
    executor = ProcessPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)


if __name__ == '__main__':
    create_logger()
    logger = logging.getLogger()

    try:
        servers = main()
    except Exception as e:
        logger.error("Undefined error in main(): %s", e)
    try:
        run(servers)
    except Exception as e:
        logger.error("Undefined error in run(): %s", e)
