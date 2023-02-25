@CD /d "%~dp0"
@ECHO OFF
@CHCP 65001

CALL venv\scripts\activate.bat
mypy main.py --python-version 3.11 --warn-return-any --warn-unused-ignores --warn-redundant-casts --no-implicit-optional --check-untyped-defs --follow-imports normal --ignore-missing-imports --disallow-untyped-defs --strict-optional
CALL venv\scripts\deactivate.bat
pause