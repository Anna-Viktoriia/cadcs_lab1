@echo off
if not exist ".venv" (
  py -3 -m venv .venv
  if errorlevel 1 (
    python -m venv .venv
  )
)
if errorlevel 1 exit /b 1

.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

.venv\Scripts\python.exe -m pytest
if errorlevel 1 exit /b 1

.venv\Scripts\pyinstaller.exe --onefile --name hello --distpath dist\ src\hello\__main__.py
if errorlevel 1 exit /b 1
