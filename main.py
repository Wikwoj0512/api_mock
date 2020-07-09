import multiprocessing
import os

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
    threads = [multiprocessing.Process(target=server.run) for server in servers]
    for thread in threads:
        thread.start()
    [thread.join() for thread in threads]


if __name__ == '__main__':
    servers = main()
    run(servers)
