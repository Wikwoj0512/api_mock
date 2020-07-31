@echo off
set service_path=%cd%/service.exe
set working_directory=%cd%
sc create MockerServiceExe binPath= "%service_path% %working_directory%" DisplayName= "MockerServiceExe" start= delayed-auto
sc description MockerServiceExe "MockerServiceExe"
sc start MockerServiceExe
