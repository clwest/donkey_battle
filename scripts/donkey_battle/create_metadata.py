from brownie import BattleDonkeyz, network
from scripts.helpful_scripts import get_name
from metadata.sample_metadata import metadata_template
from metadata.donkey_metadata_image import donkey_to_image_uri
from pathlib import Path
import json
import requests
import os


def main():
  donkey_warrior = BattleDonkeyz[-1]
  number_of_donkey_warriors = donkey_warrior.tokenCounter()
  print(f"you have created {number_of_donkey_warriors} Donkey!")
  for token_id in range(number_of_donkey_warriors):
    name = get_name(donkey_warrior.tokenIdToDonkey(token_id))
    metadata_file_name = (
      f"./metadata/{network.show_active()}/{token_id}-{name}.json"
    )
    donkey_metadata = metadata_template
    if Path(metadata_file_name).exists():
      print(f"{metadata_file_name} already exists! Delete it to overwrite")
    else:
      print(f"Creating Metadata file: {metadata_file_name}")
      donkey_metadata["name"] = name
      donkey_metadata["description"] = f"My name is {name} and I am ready to rumble!"
      image_path = "./img/" + name.lower() + ".png"
      
      image_uri = None
      if os.getenv("UPLOAD_IPFS") == "true":
          image_uri = upload_to_ipfs(image_path)
      image_uri = image_uri if image_uri else donkey_to_image_uri[name]
      
      
      donkey_metadata["image"] = image_uri
      with open(metadata_file_name, "w") as file:
          json.dump(donkey_metadata, file)
      if os.getenv("UPLOAD_IPFS") == "true":
          upload_to_ipfs(metadata_file_name)
        
      print(donkey_metadata)

def upload_to_ipfs(filepath):
  with Path(filepath).open("rb") as fp:
    image_binary = fp.read()
    ipfs_url = "http://127.0.0.1:5001"
    endpoint = "/api/v0/add"
    response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
    ipfs_hash = response.json()["Hash"]
    filename = filepath.split("/")[-1:][0]
    print(filename)
    image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
    print(image_uri)
    return image_uri
    return ipfs_hash