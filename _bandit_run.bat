@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
bandit -r main.py tests modules -n 3 -lll -f html -o check_result.html
CALL venv\scripts\deactivate.bat

pause