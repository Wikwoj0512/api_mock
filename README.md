# api_mock

Program or service working as rest API mocker based on [mockoon](https://mockoon.com/)

If ran as program, supply path for config.yaml, mockoon configuration and logs as an argument (default: directory of the program)

If ran as a service, path for config.yaml, mockoon configuration and logs can be set in createService.bat (default: directory of createService.bat)

To set host, flask debug, logging level or path to mockoon configuration, use config.yaml

Default values:

Argument | Default value | Possible values
---------|---------------|----------------
host_addr | 0.0.0.0 | Ip address of host
flask_debug | false | true, false
mockoon_file | mockoon_files/mockoon_configuration.json | relative or absolute path
logging_level | INFO | int <0;60>, CRITICAL, ERROR, WARNING, INFO, DEBUG 

To set up createService.bat: 

Variable name | Default value | Desired value
---------|---------------|----------------
python_path | %~dp0Python\python.exe | absolute path to your python.exe (python 3.7)
service_path | %~dp0service.py | absolute path to local service.py file
working_directory | %~dp0 | path for config.yaml, mockoon configuration and logs

To create service run createService.bat

To run service type **sc start MockerService** in command prompt or run it from default windows tool.

Zipped package comes with python 3.7 with installed dependencies
