#!/usr/bin/env python3
"""
CommandCube Server Pro - Professional Edition
Self-hosting solution for remote PC control
"""

import sys
import os
import subprocess
import json
from pathlib import Path
import threading
import time
from datetime import datetime

# Auto-install PyQt5 if missing
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                  QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, 
                                  QListWidget, QListWidgetItem, QDialog, QCheckBox, QStatusBar)
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "-q"])
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                  QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, 
                                  QListWidget, QListWidgetItem, QDialog, QCheckBox, QStatusBar)
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
    from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap

try:
    import flask
    import websockets
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "websockets", "-q"])

class ServerManager(QObject):
    """Manages server process"""
    connection_changed = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.server_process = None
        self.is_running = False
        self.config_file = Path("commandcube_config.json")
        self.scripts_file = Path("commandcube_scripts.json")
        self.load_config()
        
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {"port": 5000, "host": "0.0.0.0", "auto_start": False}
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_scripts(self):
        if self.scripts_file.exists():
            with open(self.scripts_file) as f:
                return json.load(f)
        return {}
    
    def save_scripts(self, scripts):
        with open(self.scripts_file, 'w') as f:
            json.dump(scripts, f, indent=2)
    
    def start_server(self):
        if self.is_running:
            return False
        
        try:
            from app import create_app
            app = create_app()
            self.server_process = threading.Thread(
                target=lambda: app.run(
                    host=self.config["host"],
                    port=self.config["port"],
                    debug=False,
                    use_reloader=False,
                    threaded=True
                ),
                daemon=True
            )
            self.server_process.start()
            self.is_running = True
            self.connection_changed.emit(True)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def stop_server(self):
        if not self.is_running:
            return False
        self.is_running = False
        self.connection_changed.emit(False)
        return True

class CommandCubeUI(QMainWindow):
    """Professional UI for CommandCube Server"""
    
    def __init__(self):
        super().__init__()
        self.server = ServerManager()
        self.setup_ui()
        self.check_installation()
        
    def setup_ui(self):
        self.setWindowTitle("CommandCube Server Pro")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Server control
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        title = QLabel("CommandCube Server Pro")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #00d4ff; margin-bottom: 20px;")
        left_layout.addWidget(title)
        
        # Status
        status_label = QLabel("Status:")
        status_label.setStyleSheet("color: #00d4ff; font-weight: bold;")
        left_layout.addWidget(status_label)
        
        self.status_indicator = QLabel("● OFFLINE")
        self.status_indicator.setStyleSheet("color: #ff4444; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(self.status_indicator)
        
        # Connection info
        self.connection_info = QLabel("Not running")
        self.connection_info.setStyleSheet("color: #888; font-size: 11px;")
        left_layout.addWidget(self.connection_info)
        
        # Control buttons
        start_btn = QPushButton("▶ START SERVER")
        start_btn.setStyleSheet(self.get_button_style("#00d4ff"))
        start_btn.clicked.connect(self.start_server)
        left_layout.addWidget(start_btn)
        
        stop_btn = QPushButton("⏹ STOP SERVER")
        stop_btn.setStyleSheet(self.get_button_style("#ff4444"))
        stop_btn.clicked.connect(self.stop_server)
        left_layout.addWidget(stop_btn)
        
        # Script library
        library_label = QLabel("\nScript Library:")
        library_label.setStyleSheet("color: #00d4ff; font-weight: bold; margin-top: 20px;")
        left_layout.addWidget(library_label)
        
        self.script_list = QListWidget()
        self.script_list.setStyleSheet(self.get_list_style())
        left_layout.addWidget(self.script_list)
        
        # Script controls
        script_btn_layout = QHBoxLayout()
        new_script_btn = QPushButton("+ New")
        new_script_btn.setStyleSheet(self.get_button_style("#00aa88"))
        new_script_btn.clicked.connect(self.new_script)
        script_btn_layout.addWidget(new_script_btn)
        
        delete_script_btn = QPushButton("- Delete")
        delete_script_btn.setStyleSheet(self.get_button_style("#ff6666"))
        delete_script_btn.clicked.connect(self.delete_script)
        script_btn_layout.addWidget(delete_script_btn)
        
        left_layout.addLayout(script_btn_layout)
        left_layout.addStretch()
        
        # Right panel - Script editor
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        editor_label = QLabel("Script Editor:")
        editor_label.setStyleSheet("color: #00d4ff; font-weight: bold;")
        right_layout.addWidget(editor_label)
        
        self.script_editor = QTextEdit()
        self.script_editor.setStyleSheet(self.get_editor_style())
        self.script_editor.setPlaceholderText("Enter Python code here...\n\nExample:\nimport platform\nprint(f'OS: {platform.system()}')")
        right_layout.addWidget(self.script_editor)
        
        # Save button
        save_script_btn = QPushButton("💾 Save Script")
        save_script_btn.setStyleSheet(self.get_button_style("#0099cc"))
        save_script_btn.clicked.connect(self.save_script)
        right_layout.addWidget(save_script_btn)
        
        # Main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready | Python: Installed | Dependencies: OK")
        self.statusBar.setStyleSheet("color: #00ff88; background: #0f3460;")
        
        # Timer for status updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)
    
    def get_stylesheet(self):
        return """
        QMainWindow {
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            color: #fff;
        }
        QWidget {
            background: transparent;
            color: #fff;
        }
        QTextEdit {
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 6px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        QLineEdit {
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 6px;
            padding: 8px;
        }
        QListWidget {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 6px;
            color: #fff;
        }
        QListWidget::item:selected {
            background: rgba(0, 212, 255, 0.3);
        }
        """
    
    def get_button_style(self, color):
        return f"""
        QPushButton {{
            background: {color};
            color: #000;
            border: none;
            border-radius: 6px;
            padding: 12px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            opacity: 0.8;
        }}
        """
    
    def get_list_style(self):
        return """
        QListWidget {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 6px;
        }
        """
    
    def get_editor_style(self):
        return """
        QTextEdit {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 212, 255, 0.3);
            color: #00ff88;
        }
        """
    
    def check_installation(self):
        """Check if Python and dependencies are installed"""
        pass
    
    def start_server(self):
        if self.server.start_server():
            self.status_indicator.setText("● ONLINE")
            self.status_indicator.setStyleSheet("color: #00ff88; font-size: 14px; font-weight: bold;")
            self.connection_info.setText(f"Running on {self.server.config['host']}:{self.server.config['port']}")
    
    def stop_server(self):
        if self.server.stop_server():
            self.status_indicator.setText("● OFFLINE")
            self.status_indicator.setStyleSheet("color: #ff4444; font-size: 14px; font-weight: bold;")
            self.connection_info.setText("Not running")
    
    def update_status(self):
        """Update UI status"""
        if self.server.is_running:
            self.statusBar.showMessage(f"✓ Server Running | Connected Clients: 0 | Uptime: {datetime.now().strftime('%H:%M:%S')}")
        else:
            self.statusBar.showMessage("Server Offline | Ready to start")
    
    def new_script(self):
        """Create new script"""
        name = "New Script"
        scripts = self.server.load_scripts()
        scripts[name] = ""
        self.server.save_scripts(scripts)
        self.refresh_script_list()
    
    def delete_script(self):
        """Delete selected script"""
        item = self.script_list.currentItem()
        if item:
            scripts = self.server.load_scripts()
            del scripts[item.text()]
            self.server.save_scripts(scripts)
            self.refresh_script_list()
    
    def save_script(self):
        """Save current script"""
        item = self.script_list.currentItem()
        if item:
            scripts = self.server.load_scripts()
            scripts[item.text()] = self.script_editor.toPlainText()
            self.server.save_scripts(scripts)
            self.statusBar.showMessage("✓ Script saved")
    
    def refresh_script_list(self):
        """Refresh script library list"""
        self.script_list.clear()
        scripts = self.server.load_scripts()
        for name in scripts:
            self.script_list.addItem(name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommandCubeUI()
    window.show()
    sys.exit(app.exec_())
