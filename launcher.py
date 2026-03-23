#!/usr/bin/env python3
"""
CommandCube Professional Launcher
Production-ready GUI for server management
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import json
from pathlib import Path
import threading
import time
import socket

class CommandCubeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("CommandCube - Professional Remote Control")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.server_process = None
        self.is_running = False
        self.config_file = Path("commandcube-config.json")
        self.load_config()
        
        self.setup_ui()
        self.check_server_status()
    
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {
                "port": 8765,
                "host": "0.0.0.0",
                "auto_start": False
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_ui(self):
        """Create GUI"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="CommandCube Remote Control", 
                         font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Server Status", padding="15")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="⚫ OFFLINE", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.pack()
        
        self.info_label = ttk.Label(status_frame, text="Not running", 
                                   font=("Arial", 10))
        self.info_label.pack()
        
        # Control Frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="15")
        control_frame.pack(fill=tk.X, pady=10)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(btn_frame, text="START SERVER", 
                                    command=self.start_server)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="STOP SERVER", 
                                   command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="Port:").pack(side=tk.LEFT, padx=5)
        self.port_var = tk.StringVar(value=str(self.config["port"]))
        port_spin = ttk.Spinbox(settings_frame, from_=1000, to=65535, 
                               textvariable=self.port_var, width=10)
        port_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(settings_frame, text="Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        # Info Frame
        info_frame = ttk.LabelFrame(main_frame, text="Info", padding="15")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_text = """
CommandCube Professional Edition

✓ Remote PC Control from Phone/Web
✓ 25 Premade Buttons
✓ Real-time Response
✓ Secure WebSocket Connection

Ready to sell!
        """
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()
    
    def start_server(self):
        """Start the server"""
        if self.is_running:
            messagebox.showinfo("Info", "Server already running")
            return
        
        try:
            port = int(self.port_var.get())
            self.config["port"] = port
            self.save_config()
            
            # Start server process
            self.server_process = subprocess.Popen(
                [sys.executable, "remote-control-pc.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.is_running = True
            self.update_status(True)
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("Success", f"Server started on port {port}")
            
            # Monitor in background
            threading.Thread(target=self.monitor_server, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start: {e}")
    
    def stop_server(self):
        """Stop the server"""
        if not self.is_running:
            return
        
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            
            self.is_running = False
            self.update_status(False)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", "Server stopped")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop: {e}")
    
    def monitor_server(self):
        """Monitor server health"""
        while self.is_running and self.server_process:
            if self.server_process.poll() is not None:
                self.is_running = False
                self.update_status(False)
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
            time.sleep(1)
    
    def check_server_status(self):
        """Check if server is responding"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.config["port"]))
            sock.close()
            return result == 0
        except:
            return False
    
    def update_status(self, running):
        """Update status display"""
        if running:
            self.status_label.config(text="🟢 ONLINE", foreground="green")
            ip = self.get_local_ip()
            self.info_label.config(text=f"Running on {ip}:{self.config['port']}")
        else:
            self.status_label.config(text="⚫ OFFLINE", foreground="red")
            self.info_label.config(text="Not running")
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def save_settings(self):
        """Save settings"""
        try:
            port = int(self.port_var.get())
            if port < 1000 or port > 65535:
                messagebox.showerror("Error", "Port must be 1000-65535")
                return
            
            self.config["port"] = port
            self.save_config()
            messagebox.showinfo("Success", "Settings saved")
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandCubeLauncher(root)
    root.mainloop()
