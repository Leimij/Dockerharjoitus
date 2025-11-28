import os
import random
import string
import hashlib
from flask import Flask, send_file, jsonify

app = Flask(__name__)

FILE_PATH = "/serverdata/randomfile.txt"

def create_random_file():
    # Luo 1KB kokoinen merkkijono
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
    
    # Kirjoitetaan teksti palvelimen voluumiin
    with open(FILE_PATH, "w") as f:
        f.write(data)

def calculate_checksum():
    # Lasketaan checksum
    sha256 = hashlib.sha256()
    with open(FILE_PATH, "rb") as f:
        sha256.update(f.read())
    return sha256.hexdigest()

# Luo tiedoston ja palauttaa sen checksum-arvon JSON-muodossa
@app.route("/generate", methods=["GET"])
def generate():
    create_random_file()
    checksum = calculate_checksum()
    return jsonify({"status": "OK", "checksum": checksum})

# Palauttaa palvelimen luoman tiedoston asiakkaalle
@app.route("/file", methods=["GET"])
def get_file():
    return send_file(FILE_PATH, as_attachment=True)

if __name__ == "__main__":
    # Varmistetaan, että hakemisto on voluumissa
    os.makedirs("/serverdata", exist_ok=True)
    
    print("Service running on port 8080...")
    app.run(host="0.0.0.0", port=8080)
