@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
pyinstaller -n="PromoDJScraper" --icon=logo.ico -w --onedir --upx-dir upx  main.py
CALL venv\scripts\deactivate.bat
COPY logo.ico dist\PromoDJScraper\
COPY LICENSE.txt dist\PromoDJScraper\
COPY README.txt dist\PromoDJScraper\
pause