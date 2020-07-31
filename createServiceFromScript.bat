@echo of
set python_path=py
set service_path=%cd%/service.py
set working_directory=%cd%

sc create MockerService binPath= "%python_path% %service_path% %working_directory%" DisplayName= "MockerService" start= delayed-auto
sc description MockerServiceExe "MockerService"
sc start MockerService



