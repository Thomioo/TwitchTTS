@echo off
REM Change directory to the location of this script
cd /d "%~dp0"

REM Optionally activate a virtual environment if you have one
REM Uncomment the next line if using a virtual environment
call venv\Scripts\activate.bat

REM Run the server
python main.py

REM Keep the command prompt open after the script finishes
pause