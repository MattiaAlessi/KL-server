# 📄 KL-server — USB-Based Keylogger & Screenshot Sender

## 🧠 Overview
**KL-server** is a modular keylogging and screenshot capture system designed for Windows. It runs silently in the background, logs keyboard input, captures periodic screenshots, and sends all data to a remote Flask server. The system is optimized for USB execution: once launched from a USB stick, it remains active even after the device is removed.

## 📁 USB Stick Contents
To run KL-server from a USB drive, include the following files:

KL-server/  
├── start.bat              ← Launches everything  
├── main.py                ← Installs dependencies and starts logger  
├── logger.py              ← Keylogger + screenshot sender (hidden)  
├── ip_address.txt         ← IP address of the receiving server (e.g. 192.168.1.42)  
└── requirements.txt       ← Required Python libraries  

## ⚙️ Setup Instructions
1. **Edit `ip_address.txt`**  
   Add the IP address of the machine running `server.py` (e.g. `192.168.1.42`)

2. **Ensure Python is installed**  
   Python must be installed and accessible via terminal (`python`) on the target machine

3. **Dependencies**  
   `main.py` will automatically install the required libraries:
   - pynput  
   - requests  
   - pyautogui  
   - pywin32  

## 🚀 How to Run
1. Insert the USB stick  
2. Double-click `start.bat`  
3. The logger will:  
   - Hide its console window  
   - Start capturing keystrokes every 10 seconds  
   - Send screenshots every 60 seconds  
   - Continue running even after the USB is removed  

## 🖥️ Flask Server (Receiver)
Run `server.py` on the receiving machine. It will:
- Save keyboard data to `received_data.txt`  
- Save screenshots to the `screenshots/` folder with incremental filenames (`Screenshot_0.png`, `Screenshot_1.png`, ...)  

> ⚠️ This project is a modified version of [David Bombal's Python Keylogger](https://github.com/davidbombal/python-keylogger/blob/main/keylogger.py), adapted for screenshot capture, stealth execution, and remote data transmission.

## 🔒 Notes
- The logger saves a local copy of each screenshot in `%APPDATA%\Local\Logger`  
- The server must be reachable via LAN or public IP  
- Both machines must be on the same network unless using port forwarding or VPN  
