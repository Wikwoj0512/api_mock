@echo off
set python_path=py
set service_path=%~dp0service.py
set working_directory=%~dp0

"%python_path%" -m pip install -U -r requirements.txt

sc create MockerService binPath= "%python_path% %service_path% %working_directory%"



