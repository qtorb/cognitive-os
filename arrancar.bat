@echo off
cd /d "%~dp0"
cd backend
pip install -r requirements.txt
python main.py
pause
