@echo off
rem Command line Solaar, e.g.:  solaar-cli show   or   solaar-cli config G733 sidetone 50
set "GI_TYPELIB_PATH=%~dp0runtime\lib\girepository-1.0"
"%~dp0runtime\bin\python.exe" "%~dp0app\bin\solaar" %*
