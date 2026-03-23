#!/usr/bin/env python3
"""CommandCube Installer"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

def install():
    print("=" * 50)
    print("CommandCube Professional Installer")
    print("=" * 50)
    
    # Create Program Files directory
    program_dir = Path(r"C:\Program Files\CommandCube")
    
    print(f"\n[1/5] Creating directories...")
    program_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[2/5] Copying files...")
    files = ["launcher.py", "remote-control-pc.py", "index.html", "CommandCube-Remote.apk"]
    for f in files:
        src = Path(f)
        dst = program_dir / f
        if src.exists():
            shutil.copy(src, dst)
            print(f"     ✓ {f}")
    
    print(f"\n[3/5] Creating shortcuts...")
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "CommandCube.lnk"
    print(f"     Shortcut: {shortcut_path}")
    
    print(f"\n[4/5] Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "websockets"])
    print(f"     ✓ Dependencies installed")
    
    print(f"\n[5/5] Creating start script...")
    bat_file = program_dir / "START.bat"
    bat_file.write_text(f"""@echo off
cd /d "{program_dir}"
python launcher.py
pause
""")
    print(f"     ✓ {bat_file}")
    
    print(f"\n" + "=" * 50)
    print(f"Installation Complete!")
    print(f"=" * 50)
    print(f"\nProgram installed to: {program_dir}")
    print(f"Start launcher: {bat_file}")
    print(f"\nRun 'START.bat' to launch CommandCube")
    
if __name__ == "__main__":
    try:
        install()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
