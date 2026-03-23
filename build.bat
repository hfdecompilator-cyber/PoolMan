@echo off
REM CommandCube Server Pro - Build EXE
REM This converts Python to standalone Windows executable

echo [CommandCube] Installing build tools...
pip install pyinstaller -q

echo [CommandCube] Building executable...
pyinstaller --onefile ^
    --windowed ^
    --name "CommandCube Server Pro" ^
    --icon=icon.ico ^
    --add-data "app.py:." ^
    --hidden-import=PyQt5 ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    server_pro.py

echo [CommandCube] Build complete!
echo Output: dist\CommandCube Server Pro.exe
pause
