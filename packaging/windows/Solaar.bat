@echo off
rem Starts the Solaar window without a console. Extra arguments are passed through (e.g. --window=hide).
set "GI_TYPELIB_PATH=%~dp0runtime\lib\girepository-1.0"
start "" "%~dp0runtime\bin\pythonw.exe" "%~dp0app\bin\solaar" %*
