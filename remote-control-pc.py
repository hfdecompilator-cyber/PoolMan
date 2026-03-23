#!/usr/bin/env python3
"""CommandCube - Execute ANY Python Script"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

try:
    import websockets
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

async def execute_script(script_code):
    """Execute ANY Python script"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", script_code],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "Script timeout (30s max)"
    except Exception as e:
        return f"Error: {str(e)}"

async def handle(ws):
    """Handle WebSocket connection"""
    try:
        async for msg in ws:
            data = json.loads(msg)
            
            # Accept ANY Python code
            script = data.get("script") or data.get("code")
            
            if script:
                output = await execute_script(script)
                await ws.send(json.dumps({"output": output}))
            else:
                await ws.send(json.dumps({"error": "No script provided"}))
    except:
        pass

async def main():
    """Start server"""
    print("[+] CommandCube - Python Script Executor")
    print("[+] Port: 8765")
    print("[+] Ready to execute ANY Python code\n")
    
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Stopped")
