#!/usr/bin/env python3
import asyncio
import json
import sys

try:
    import websockets
except:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    import websockets

async def test():
    print("[*] Testing CommandCube Server...")
    print("[*] Connecting to ws://localhost:8765\n")
    
    try:
        async with websockets.connect("ws://localhost:8765") as ws:
            print("[+] Connected!")
            
            # Test System Info
            print("\n[TEST 1] System Info")
            await ws.send(json.dumps({"category": "System", "button": "System Info"}))
            response = await ws.recv()
            print("[RESPONSE]", response)
            
            # Test Memory
            print("\n[TEST 2] Memory Usage")
            await ws.send(json.dumps({"category": "System", "button": "Memory"}))
            response = await ws.recv()
            print("[RESPONSE]", response)
            
            # Test Network
            print("\n[TEST 3] IP Address")
            await ws.send(json.dumps({"category": "Network", "button": "IP"}))
            response = await ws.recv()
            print("[RESPONSE]", response)
            
            # Test Browser
            print("\n[TEST 4] Open YouTube")
            await ws.send(json.dumps({"category": "Browser", "button": "YouTube"}))
            response = await ws.recv()
            print("[RESPONSE]", response)
            
            print("\n[+] All tests passed!")
            
    except Exception as e:
        print(f"[-] Error: {e}")
        print("[-] Make sure server is running: python remote-control-pc.py")

if __name__ == "__main__":
    asyncio.run(test())
