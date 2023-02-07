@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
pyright -p . 
CALL venv\scripts\deactivate.bat

pause