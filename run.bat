@echo off
if not exist ".venv" (
  py -3 -m venv .venv
  if errorlevel 1 (
    python -m venv .venv
  )
  if errorlevel 1 exit /b 1

  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 exit /b 1
)

set PYTHONPATH=src
.venv\Scripts\python.exe -m hello
if errorlevel 1 exit /b 1
