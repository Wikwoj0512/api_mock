@echo off
set service_path=%~dp0service.exe
set working_directory=%~dp0

sc create MockerServiceExe binPath= "%service_path% %working_directory%"



