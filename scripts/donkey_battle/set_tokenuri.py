from brownie import network, BattleDonkeyz
from scripts.helpful_scripts import get_name, get_account, OPENSEA_URL


donkey_metadata_dic = {
"BUSTA": "https://ipfs.io/ipfs/QmTtB5A81j4acbGLU4Etnhf11UKWpJzAgZgDJU39Ztet4v?filename=0-BUSTA.json",
"REBEL": "https://ipfs.io/ipfs/QmbZjdhuwKcArzV1JTPFh122AscRZvt9RYiqMLU3KowHnz?filename=1-REBEL.json",
"JETHRO": "https://ipfs.io/ipfs/QmYXRzfBAXSA8Dh2QvnzprhKvUAqdEyeDTqtb46aBumDXD?filename=2-JETHRO.json",
"ROSCOE": "https://ipfs.io/ipfs/QmTA1sqLdsVgV91oiST2DogK4PLjfwq1v4dM3esUSvk4BA?filename=3-ROSCOE.json",
"TWEAK": "https://ipfs.io/ipfs/QmefsrvJ5h8MZ42FxHq4FebG5x7c3d3XRD5tegreTbbLVx?filename=4-TWEAK.json",
  
}


def main():
  print(f"Working on {network.show_active()}")
  donkey_warrior = BattleDonkeyz[-1]
  number_of_donkeys = donkey_warrior.tokenCounter()
  print(f"You have {number_of_donkeys} tokenIds")
  for token_id in range(number_of_donkeys):
    name = get_name(donkey_warrior.tokenIdToDonkey(token_id))
    if not donkey_warrior.tokenURI(token_id).startswith("https://"):
      print(f"Setting tokenURI of {token_id}")
      set_tokenURI(token_id, donkey_warrior, donkey_metadata_dic[name])
      
def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes, and hit the refresh metadata button")