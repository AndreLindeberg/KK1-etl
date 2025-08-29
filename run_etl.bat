@echo off
setlocal
pushd "%~dp0"

set "PY=%~dp0venv\Scripts\python.exe"
if exist "%PY%" (set "CMD=%PY%") else (set "CMD=python")

"%CMD%" "%~dp0main.py" --csv "%~dp0data\sales.csv" --db "%~dp0data\etl.db"
set "RC=%ERRORLEVEL%"

popd
exit /b %RC%
