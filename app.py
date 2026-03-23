#!/usr/bin/env python3
"""CommandCube API Server - Ready for OnSpace AI"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CommandCube - Remote PC Control</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
                color: #fff;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                max-width: 700px;
                width: 100%;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 40px;
                backdrop-filter: blur(10px);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                background: linear-gradient(135deg, #00d4ff, #0099cc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 28px;
            }
            .section {
                margin-bottom: 30px;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: 600;
                color: #00d4ff;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 1px;
            }
            textarea {
                width: 100%;
                height: 200px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #fff;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                resize: vertical;
            }
            textarea:focus {
                outline: none;
                border-color: #00d4ff;
                box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
            }
            .buttons {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            button {
                padding: 12px 20px;
                background: linear-gradient(135deg, #00d4ff, #0099cc);
                border: none;
                border-radius: 8px;
                color: #000;
                font-weight: 600;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 13px;
                transition: all 0.3s ease;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .output-label { color: #00d4ff; }
            .output {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
                min-height: 150px;
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #00ff88;
            }
            .output.loading { color: #00d4ff; }
            .output.error { color: #ff4444; }
            .presets {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 15px;
            }
            .preset-btn {
                padding: 10px;
                background: rgba(0, 212, 255, 0.1);
                border: 1px solid rgba(0, 212, 255, 0.3);
                border-radius: 6px;
                color: #00d4ff;
                cursor: pointer;
                font-size: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .preset-btn:hover {
                background: rgba(0, 212, 255, 0.2);
                border-color: #00d4ff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ CommandCube Remote Control</h1>
            
            <div class="section">
                <label>Python Script</label>
                <textarea id="code" placeholder="Enter Python code...
Example:
import platform
print(f'OS: {platform.system()}')"></textarea>
            </div>
            
            <div class="section">
                <label>Presets</label>
                <div class="presets">
                    <button class="preset-btn" onclick="loadPreset('system')">System Info</button>
                    <button class="preset-btn" onclick="loadPreset('time')">Get Time</button>
                    <button class="preset-btn" onclick="loadPreset('files')">List Files</button>
                    <button class="preset-btn" onclick="loadPreset('ip')">Get IP</button>
                </div>
            </div>
            
            <div class="section">
                <div class="buttons">
                    <button onclick="runCode()">Execute</button>
                    <button onclick="clearCode()">Clear</button>
                </div>
            </div>
            
            <div class="section">
                <label class="output-label">Output</label>
                <div class="output" id="output">Ready...</div>
            </div>
        </div>

        <script>
            const presets = {
                'system': 'import platform\\nprint(f"OS: {platform.system()}")\\nprint(f"Processor: {platform.processor()}")',
                'time': 'from datetime import datetime\\nprint(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))',
                'files': 'from pathlib import Path\\nfiles = list(Path.home().glob("*"))[:10]\\nfor f in files: print(f.name)',
                'ip': 'import socket\\nprint(socket.gethostbyname(socket.gethostname()))'
            };

            async function runCode() {
                const code = document.getElementById('code').value;
                const output = document.getElementById('output');
                
                if (!code.trim()) {
                    output.textContent = 'Enter code first';
                    output.className = 'output error';
                    return;
                }
                
                output.textContent = 'Executing...';
                output.className = 'output loading';
                
                try {
                    const response = await fetch('/api/execute', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ script: code })
                    });
                    
                    const data = await response.json();
                    output.textContent = data.output || 'No output';
                    output.className = 'output';
                } catch (e) {
                    output.textContent = 'Error: ' + e.message;
                    output.className = 'output error';
                }
            }
            
            function clearCode() {
                document.getElementById('code').value = '';
                document.getElementById('output').textContent = 'Ready...';
                document.getElementById('output').className = 'output';
            }
            
            function loadPreset(preset) {
                document.getElementById('code').value = presets[preset];
            }
            
            window.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') runCode();
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/execute', methods=['POST'])
def execute():
    """Execute Python script"""
    try:
        data = request.json
        script = data.get('script', '')
        
        if not script:
            return jsonify({'error': 'No script provided'}), 400
        
        result = subprocess.run(
            [sys.executable, '-c', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += result.stderr
        
        return jsonify({'output': output or 'Script executed'})
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Script timeout (30s max)'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check if server is running"""
    return jsonify({'status': 'online', 'version': '1.0'})

if __name__ == '__main__':
    print("[+] CommandCube API Server")
    print("[+] http://localhost:5000")
    print("[+] Ready for OnSpace AI deployment\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
