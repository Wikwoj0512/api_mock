import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

from models.configuration import Configuration
from models.logger import create_logger
from server import Server

if "logs" not in os.listdir(): os.mkdir("logs")

HOST = "0.0.0.0"
DEBUG = False
CONFIGURATION_FILE = 'znaki.json'


def main():
    create_logger()

    configuration = Configuration(f"mockoon_files/{CONFIGURATION_FILE}")
    environments = configuration.load_configuration()
    servers = [Server.factory(HOST, environment) for environment in environments]

    return servers


def run(servers):
    executor = ProcessPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)


if __name__ == '__main__':
    servers = main()
    run(servers)
