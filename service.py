import socket

import servicemanager
import win32event
import win32service
import win32serviceutil

from main import main as appMain
from main import run as appRun
from models.logger import create_logger
from models.models_file import AppConfiguration


class HelloWorldSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "mock-api"
    _svc_display_name_ = "Mock API"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

        self.stop_requested = True
        for proc in self.processes:
            proc.kill()
            proc.terminate()

    def SvcDoRun(self):

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        config = AppConfiguration.fromFile("config.yaml")
        logger = create_logger(level=config.logging_level)
        try:
            servers = appMain(config)
        except Exception as e:
            logger.error("Undefined error in main(): %s", e)
        try:
            processes = appRun(servers)
        except Exception as e:
            logger.error("Undefined error in run(): %s", e)

        self.processes = processes
        [proc.start() for proc in processes]
        [proc.join() for proc in processes]


if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(HelloWorldSvc)
    servicemanager.StartServiceCtrlDispatcher()
