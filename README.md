# api_mock

Program or service working as rest API mocker based on [mockoon](https://mockoon.com/)

Available Mockoon helpers are:
* queryParam
* urlParam
* header
* hostname
* ip
* method

If main.py is ran as script, it gets the current working directory as path for config.yaml, mockoon configuration and logs, unless another path is added as argument

To create windows service from .py script, run createServiceFromScript.bat. 
> This creates MockerService service

To create executable package run createExeDir.bat. It will automatically create an .exe file from service and put it in servicePackage directory along with config.yaml, mockoon_files and createServiceFromExe.bat.
>Building executable file requires installed [pyinstaller](https://www.pyinstaller.org/) and working from path

To create windows service from .exe file, run createServiceFromExe.bat in ServicePackage directory.
> This creates MockerServiceExe service

To set host, flask debug, logging level or path to mockoon configuration, use config.yaml

Default values:

Argument | Default value | Possible values
---------|---------------|----------------
host_addr | 0.0.0.0 | Ip address of host
flask_debug | false | true, false
mockoon_file | mockoon_files/mockoon_configuration.json | relative or absolute path
logging_level | INFO | int <0;60>, CRITICAL, ERROR, WARNING, INFO, DEBUG 



To set up createServiceFromScript.bat: 

Variable name | Default value | Desired value
---------|---------------|----------------
python_path | py | absolute path to your python.exe (python 3.7) or console argument if python is in path
service_path | %~dp0service.py | absolute path to local service.py file
working_directory | %~dp0 | path for config.yaml, mockoon configuration and logs



To set up createServiceFromExe.bat: 

Variable name | Default value | Desired value
---------|---------------|----------------
service_path | %~dp0service.py | absolute path to service.exe file
working_directory | %~dp0 | path for config.yaml, mockoon configuration and logs

