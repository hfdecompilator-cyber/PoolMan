#!/usr/bin/env python3
"""CommandCube - Simple HTTP Server"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import sys
from pathlib import Path

class Handler(BaseHTTPRequestHandler):
    """Handle HTTP requests"""
    
    def do_GET(self):
        """Serve HTML"""
        if self.path == "/" or self.path == "/index.html":
            try:
                html = Path("index.html").read_text(encoding='utf-8')
            except:
                html = "<h1>CommandCube</h1><p>Server running</p>"
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Execute Python scripts"""
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            
            script = data.get("script") or data.get("code", "")
            
            if not script:
                response = {"error": "No script"}
            else:
                try:
                    result = subprocess.run(
                        [sys.executable, "-c", script],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    response = {"output": result.stdout + result.stderr}
                except subprocess.TimeoutExpired:
                    response = {"output": "Script timeout (30s max)"}
                except Exception as e:
                    response = {"error": str(e)}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        except Exception as e:
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress logs"""
        pass

if __name__ == "__main__":
    PORT = 8080
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[+] CommandCube Server")
    print(f"[+] Open: http://localhost:{PORT}")
    print(f"[+] Ready to execute ANY Python code\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopped")
