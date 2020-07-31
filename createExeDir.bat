@echo off

RMDIR/Q/S build

pyinstaller --noconfirm --onefile --console --hidden-import "pkg_resources.py2_warn" --hidden-import "Flask" --hidden-import "PyYAML" --hidden-import "pywin32"  .\service.py


mkdir .\dist\mockoon_files
COPY .\mockoon_files .\dist\mockoon_files
copy createServiceFromExe.bat /B .\dist
copy config.yaml /A .\dist

DEL service.spec