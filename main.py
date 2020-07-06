from configuration import Configuration, Server
from multiprocessing.dummy import Pool as ThreadPool
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


HOST = "0.0.0.0"
DEBUG = False
CONFIGURATION_FILE = 'mocoon.json'

def main():
    configuration = Configuration(f"mockoon_files/{CONFIGURATION_FILE}")
    environments = configuration.load_configuration()

    servers = [Server(HOST, DEBUG, environment) for environment in environments]
    apps = [server.setup() for server in servers]

    return servers, apps



def run(servers):
    executor = ThreadPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)

if __name__ == '__main__':
    servers, apps = main()
    run(servers)
