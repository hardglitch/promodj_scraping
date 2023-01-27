@CHCP 65001
@echo off

pipenv run pyinstaller -n="PDJ_Scraper" --icon=logo.ico --onefile -w main.py

pause