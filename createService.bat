@echo off
set python_path=%~dp0Python\python.exe
set service_path=%~dp0service.py
set working_directory=%~dp0

"%pythonpath%" -m pip install -U -r requirements.txt

sc create MockerService binPath= "%python_path% %service_path% %working_directory%"



