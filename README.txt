# CommandCube Remote Control - Complete Package

## What's Here

- **remote-control-pc.py** - Server (MUST RUN FIRST)
- **CommandCube-Remote.apk** - Android app for phone
- **index.html** - Web browser interface
- **build-apk.py** - APK builder script

---

## QUICK START (3 Steps)

### 1. START THE SERVER
```
python remote-control-pc.py
```
Wait for message: "CommandCube Remote Control Ready!"

### 2. CHOOSE YOUR CONTROL METHOD

**Option A - WEB BROWSER (Easiest)**
- Open: http://localhost:8080
- Enter PC IP
- Click Connect
- Use buttons

**Option B - ANDROID PHONE**
- Transfer: CommandCube-Remote.apk to phone
- Install (Settings > Security > Unknown Sources)
- Open app
- Enter PC IP
- Click Connect

### 3. USE THE BUTTONS
25 commands across 6 categories:
- System (Info, Memory, CPU, Speed, Uptime)
- Files (Documents, Large, Desktop, Downloads, Recent)
- Control (Shutdown, Restart, Lock, Sleep, Volume)
- Network (IP, WiFi, Speed, Ping, DNS)
- Browser (YouTube, Google, GitHub, ChatGPT, Gmail)
- Apps (Notepad, Calc, Paint, PowerShell, TaskMgr)

---

## TROUBLESHOOTING

**APK won't install?**
- Enable Unknown Sources: Settings > Security > Unknown Sources
- Try CommandCube-Remote.apk (newer version)

**Can't connect?**
- Make sure server is running
- Check PC IP address
- Firewall may block port 8765

**Server won't start?**
- Make sure Python 3 is installed
- Try: python3 remote-control-pc.py

---

## FILES EXPLAINED

- remote-control-pc.py: Main server (HTTP + WebSocket)
- index.html: Web UI (open in browser)
- CommandCube-Remote.apk: Android app
- build-apk.py: Script to rebuild APK if needed

---

## PORTS

- Port 8080: HTTP (web interface)
- Port 8765: WebSocket (button commands)

Both needed for full functionality.

---

Start with: python remote-control-pc.py
Then visit: http://localhost:8080
