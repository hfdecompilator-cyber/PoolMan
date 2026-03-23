#!/usr/bin/env python3
import http.server
import socketserver
import json
import subprocess
import sys

PORT = 9000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        
        try:
            data = json.loads(body)
            script = data.get("script", "")
            
            result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
        except:
            output = "Error"
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"output": output}).encode())

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[+] Running on port {PORT}")
    httpd.serve_forever()
