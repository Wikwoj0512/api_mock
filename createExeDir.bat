@echo off
py -m pip install --upgrade -r requirements.txt
py -m pip install pyinstaller

pyinstaller --noconfirm --onefile --console --hidden-import "pkg_resources.py2_warn" --hidden-import "Flask" --hidden-import "PyYAML" --hidden-import "pywin32"  .\service.py

mkdir ServicePackage

COPY .\dist\service.exe /B .\ServicePackage
mkdir .\ServicePackage\mockoon_files
COPY .\mockoon_files .\ServicePackage\mockoon_files
copy createServiceFromExe.bat /B .\ServicePackage
copy config.yaml /A .\ServicePackage

RMDIR/Q/S build
RMDIR/Q/S dist
DEL service.spec