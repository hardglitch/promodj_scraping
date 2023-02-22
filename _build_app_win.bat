@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
pyinstaller -n="PromoDJScraper" --icon=logo.ico -w --onefile --upx-dir upx  main.py
CALL venv\scripts\deactivate.bat
COPY logo.ico dist\
COPY LICENSE.txt dist\
COPY README.txt dist\
pause