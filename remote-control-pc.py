#!/usr/bin/env python3
"""CommandCube Server - Executes Custom Scripts"""

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

def load_commands():
    """Load commands from customization file"""
    config = Path("commands.json")
    if config.exists():
        with open(config) as f:
            return json.load(f)
    return {}

COMMANDS = load_commands()

async def execute_command(category, button):
    """Execute command and return output"""
    try:
        if category not in COMMANDS or button not in COMMANDS[category]:
            return "Command not found"
        
        script = COMMANDS[category][button]
        
        # Run as Python script
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.stdout or result.stderr or "Executed"
    
    except subprocess.TimeoutExpired:
        return "Command timeout"
    except Exception as e:
        return f"Error: {str(e)}"

async def handle(ws):
    """Handle WebSocket connection"""
    try:
        async for msg in ws:
            data = json.loads(msg)
            category = data.get("category")
            button = data.get("button")
            
            output = await execute_command(category, button)
            await ws.send(json.dumps({"output": output}))
    except:
        pass

async def main():
    """Start server"""
    print("[+] CommandCube Server")
    print("[+] Port: 8765")
    print(f"[+] Commands: {sum(len(v) for v in COMMANDS.values())}")
    print("[+] Ready to execute scripts\n")
    
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Stopped")
