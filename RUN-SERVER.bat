@echo off
REM CommandCube Test Script
cd /d "%~dp0"
echo Starting CommandCube Server Test...
echo.
python remote-control-pc.py
pause
