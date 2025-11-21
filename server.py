from flask import Flask, request
import os
import threading
import logging
from pyngrok import ngrok 
from termcolor import colored

app = Flask(__name__)

save_path = "screenshots"
os.makedirs(save_path, exist_ok=True)

counter_file = os.path.join(save_path, "counter.txt")

lock = threading.Lock()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_next_index():
    with lock:
        if not os.path.exists(counter_file):
            with open(counter_file, "w") as f:
                f.write("0")
            return 0
        with open(counter_file, "r+") as f:
            index = int(f.read())
            f.seek(0)
            f.write(str(index + 1))
            f.truncate()
            return index

@app.route('/', methods=['POST'])
def ricevi_testo():
    data = request.get_json()
    logging.info(f"Received text: {data}")
    with open("received_data.txt", "a", encoding="utf-8") as file:
        file.write(str(data) + "\n")
    return {"status": "ok"}

@app.route('/screenshot', methods=['POST'])
def ricevi_immagine():
    if 'file' not in request.files:
        return {"status": "error", "message": "No file uploaded"}, 400

    file = request.files['file']
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return {"status": "error", "message": "Invalid file type"}, 400

    index = get_next_index()
    ext = os.path.splitext(file.filename)[1].lower()
    filename = os.path.join(save_path, f"Screenshot_{index}{ext}")
    file.save(filename)
    logging.info(f"Screenshot received: {filename} from {request.remote_addr}")
    return {"status": "ok"}

if __name__ == "__main__":
    port = 56860
    public_url = ngrok.connect(port)
    print(colored(f"{public_url}", "cyan"))

    app.run(host='0.0.0.0', port=port)
