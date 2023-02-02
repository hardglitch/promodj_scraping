@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
pyinstaller -n="PromoDJScraper" --icon=logo.ico -w main.py
CALL venv\scripts\deactivate.bat
COPY logo.ico dist\PromoDJScraper\
pause