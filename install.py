#!/usr/bin/env python3
"""
CommandCube Installation Manager
Auto-installs Python, dependencies, and sets up environment
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class Installer:
    def __init__(self):
        self.config = {}
        
    def log(self, message):
        print(f"[CommandCube Installer] {message}")
    
    def check_python(self):
        """Check if Python is installed"""
        self.log("Checking Python installation...")
        try:
            version = f"{sys.version_info.major}.{sys.version_info.minor}"
            self.log(f"✓ Python {version} detected")
            return True
        except:
            self.log("✗ Python not found")
            return False
    
    def install_dependencies(self):
        """Install required Python packages"""
        self.log("Installing dependencies...")
        packages = ["flask", "flask-cors", "PyQt5", "websockets"]
        
        for package in packages:
            self.log(f"  Installing {package}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.log(f"  ✓ {package} installed")
            except Exception as e:
                self.log(f"  ✗ Failed to install {package}: {e}")
                return False
        
        return True
    
    def setup_environment(self):
        """Setup environment and directories"""
        self.log("Setting up environment...")
        
        # Create necessary directories
        dirs = ["scripts", "config", "logs"]
        for d in dirs:
            Path(d).mkdir(exist_ok=True)
        
        # Create default config
        config = {
            "port": 5000,
            "host": "0.0.0.0",
            "auto_start": False,
            "version": "1.0.0"
        }
        
        with open("commandcube_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        self.log("✓ Environment configured")
        return True
    
    def create_shortcut(self):
        """Create desktop shortcut (Windows only)"""
        if platform.system() == "Windows":
            self.log("Creating desktop shortcut...")
            try:
                desktop = Path.home() / "Desktop"
                script_path = Path.cwd() / "server_pro.py"
                
                batch_file = desktop / "CommandCube Server.bat"
                batch_file.write_text(f'@echo off\ncd /d "{Path.cwd()}"\npython server_pro.py\npause')
                
                self.log("✓ Shortcut created")
            except Exception as e:
                self.log(f"✗ Could not create shortcut: {e}")
    
    def run(self):
        """Run full installation"""
        print("\n" + "="*50)
        print("CommandCube Server Pro - Installation")
        print("="*50 + "\n")
        
        if not self.check_python():
            self.log("ERROR: Python is required")
            return False
        
        if not self.install_dependencies():
            self.log("ERROR: Failed to install dependencies")
            return False
        
        if not self.setup_environment():
            self.log("ERROR: Failed to setup environment")
            return False
        
        self.create_shortcut()
        
        print("\n" + "="*50)
        print("✓ Installation Complete!")
        print("="*50)
        print("\nYou can now run: python server_pro.py")
        print("\n")
        
        return True

if __name__ == "__main__":
    installer = Installer()
    success = installer.run()
    
    if success:
        input("Press Enter to continue...")
    else:
        input("Installation failed. Press Enter to exit...")
        sys.exit(1)
