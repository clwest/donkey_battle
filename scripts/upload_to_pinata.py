import requests
import os
from pathlib import Path
import json
import time


PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
filepath = './img/donkey_images'
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}

def main():
  donkey_image_path = Path(filepath).glob('**/*.png')
  for donkey_path in donkey_image_path:
    filename = str(donkey_path).split('/')[-1:][0]
    upload_to_pinata(donkey_path, filename=filename)
    
def upload_to_pinata(donkey_path, filename=None):
  with donkey_path.open("rb") as fp:
    image_binary = fp.read()
    filename = filename if filename else donkey_path
    print(f"Uploading {filename}")
    try:
      response = requests.post(PINATA_BASE_URL + endpoint,
                                files={"file": (filename, image_binary)},
                                headers=headers)
      print(response.json())
    except json.decoder.JSONDecodeError:
      print("Error, I screwed something up! ")
      time.sleep(5)
      upload_to_pinata(donkey_path, filename=filename)