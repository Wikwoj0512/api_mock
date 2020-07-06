from configuration import Configuration, Server
from multiprocessing.dummy import Pool as ThreadPool
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

HOST = "localhost"
DEBUG = False

def main():
    configuration = Configuration("C:\\Users\\Wiktor Wojtkowiak\\Desktop\\mocoon.json")
    environments = configuration.load_configuration()

    servers = [Server(HOST, DEBUG, environment) for environment in environments]
    apps = [server.setup() for server in servers]

    return servers, apps



def run(servers):
    # threads = [multiprocessing.Process(target=server.run) for server in servers]
    # for thread in threads:
    #     thread.start()
    # _ = [thread.join() for thread in threads]

    executor = ThreadPoolExecutor(max_workers=len(servers))
    for server in servers:
        executor.submit(server.run)

if __name__ == '__main__':
    servers, apps = main()
    run(servers)
