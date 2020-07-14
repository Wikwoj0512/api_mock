import os
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING

from models.configuration import ServicesConfiguration
from models.logger import create_logger
from models.models_file import AppConfiguration
from server import Server

if TYPE_CHECKING:
    from typing import List

if "logs" not in os.listdir(): os.mkdir("logs")





def main(config) -> 'List[Server]':
    create_logger()

    configuration = ServicesConfiguration(config.mockoon_file)
    environments = configuration.load_configuration()
    servers = [Server.factory(config.host, environment, debug=config.flask_debug, logging_level=config.logging_level)
               for
               environment in environments]

    return servers


def run(servers: 'List[Server]') -> None:
    executor = ProcessPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)


if __name__ == '__main__':
    config = AppConfiguration.fromFile("config.yaml")
    logger = create_logger(level=config.logging_level)
    try:
        servers = main(config)
    except Exception as e:
        logger.error("Undefined error in main(): %s", e)
    try:
        run(servers)
    except Exception as e:
        logger.error("Undefined error in run(): %s", e)
