from models.configuration import Configuration
from server import Server
from concurrent.futures import ThreadPoolExecutor
from models.logger import create_logger

HOST = "0.0.0.0"
DEBUG = False
CONFIGURATION_FILE = 'mocoon.json'



def main():
    configuration = Configuration(f"mockoon_files/{CONFIGURATION_FILE}")
    create_logger()

    environments = configuration.load_configuration()
    servers = [Server.factory(HOST, environment) for environment in environments]

    return servers



def run(servers):
    executor = ThreadPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)

if __name__ == '__main__':
    servers = main()
    run(servers)
