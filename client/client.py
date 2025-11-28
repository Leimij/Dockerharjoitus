import requests
import os

SERVER_URL = "http://servercontainer:8080"
DOWNLOAD_PATH = "/clientdata/randomfile.txt"

def main():
    print("Connecting to server...")

    # Pyydetään palvelinta luomaan tiedosto ja palauttamaan checksum
    resp = requests.get(f"{SERVER_URL}/generate")
    data = resp.json()
    checksum = data["checksum"]
    print("Checksum from server:", checksum)

    # Tietoston lataaminen
    file_resp = requests.get(f"{SERVER_URL}/file")

    os.makedirs("/clientdata", exist_ok=True)
    with open(DOWNLOAD_PATH, "wb") as f:
        f.write(file_resp.content)

    print("File downloaded and saved to /clientdata/randomfile.txt")
    print("DONE.")

if __name__ == "__main__":
    main()
