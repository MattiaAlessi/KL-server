from flask import Flask, request
import os

app = Flask(__name__)

save_path = "screenshots"
os.makedirs(save_path, exist_ok=True)

counter_file = os.path.join(save_path, "counter.txt")

def get_next_index():
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
    print("Received text:", data)
    with open("received_data.txt", "a", encoding="utf-8") as file:
        file.write(str(data) + "\n")
    return {"status": "ok"}

@app.route('/screenshot', methods=['POST'])
def ricevi_immagine():
    file = request.files['file']
    index = get_next_index()
    filename = os.path.join(save_path, f"Screenshot_{index}.png")
    file.save(filename)
    print(f"Screenshot received: {filename}")
    return {"status": "ok"}

app.run(host='0.0.0.0', port=8080)
