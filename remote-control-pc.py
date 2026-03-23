#!/usr/bin/env python3
"""CommandCube Server - Reads Custom Commands"""

import asyncio
import json
from pathlib import Path

try:
    import websockets
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

def load_commands():
    """Load commands from customization file"""
    config = Path("commands.json")
    if config.exists():
        with open(config) as f:
            return json.load(f)
    
    # Default commands
    return {
        "System": {"System Info": "print('OK')", "Memory": "print('OK')"},
        "Files": {"Documents": "print('OK')", "Desktop": "print('OK')"},
        "Control": {"Shutdown": "print('OK')", "Restart": "print('OK')"},
        "Network": {"IP": "print('OK')", "Ping": "print('OK')"},
        "Browser": {"YouTube": "print('OK')", "Google": "print('OK')"},
        "Apps": {"Notepad": "print('OK')", "Calc": "print('OK')"}
    }

COMMANDS = load_commands()

async def handle(ws):
    """Handle WebSocket connection"""
    try:
        async for msg in ws:
            data = json.loads(msg)
            await ws.send(json.dumps({"ok": True}))
    except:
        pass

async def main():
    """Start server"""
    print("[+] CommandCube Server Running")
    print(f"[+] Port: 8765")
    print(f"[+] Commands loaded: {sum(len(v) for v in COMMANDS.values())}")
    
    async with websockets.serve(handle, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Stopped")
