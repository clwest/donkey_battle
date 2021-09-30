from brownie import network, BattleDonkeyz
from scripts.helpful_scripts import get_name, get_account, OPENSEA_URL
from metadata.donkey_metadata import donkey_metadata_dic

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