import socket

import servicemanager
import win32event
import win32service
import win32serviceutil

from multiprocessing import Process
from main import main as appMain
from utils.logger import create_logger
from models.models_file import AppConfiguration


class MockerServiceSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "MockerService"
    _svc_display_name_ = "API Mocker Service"

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
        sequence = appMain()
        processes = next(sequence)
        self.processes = processes
        start = next(sequence)


if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MockerServiceSvc)
    servicemanager.StartServiceCtrlDispatcher()
