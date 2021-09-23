from brownie import network, BattleDonkeyz
from scripts.helpful_scripts import get_name, get_account, OPENSEA_URL


donkey_metadata_dic = {
"BUSTA": "https://ipfs.io/ipfs/QmdHoMucYyNZunrwb9C6pTtaxKHtbt21NZ6k3Z5Zmbwfqz?filename=0-BUSTA.json",
"REBEL": "https://ipfs.io/ipfs/QmU6HSBhQ3JXwRpVH6r7XmmSRCdoayPdsKhQkYW6t9NAyW?filename=2-REBEL.json",
"JETHRO": "https://ipfs.io/ipfs/QmfDR6vLkwoiRmjtm1W8p5SWRM6WnJcKTKpbE4EY3Ptrjq?filename=0-JETHRO.json",
"ROSCOE": "https://ipfs.io/ipfs/QmTPnC5jksNDyYnPbpZRDzMREg3PFxFqGEYuSh1KNhhyLH?filename=1-ROSCOE.json",
"TWEAK": "https://ipfs.io/ipfs/Qmetcvp6978S9KJLX4EzSiKukEb2m7Hzzv3XwrVxbsX49L?filename=0-TWEAK.json",
  
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