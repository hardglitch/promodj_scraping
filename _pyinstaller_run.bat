@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
pyinstaller -n="PDJ_Scraper" --icon=logo.ico --onefile -w main.py
CALL venv\scripts\deactivate.bat

pause