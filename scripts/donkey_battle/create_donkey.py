from brownie import BattleDonkeyz, config, network
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    donkey_warrior = BattleDonkeyz[-1]
    fund_with_link(donkey_warrior.address, amount = Web3.toWei(0.1, "ether"))
    creation_transaction = donkey_warrior.createDonkey({"from": account})
    publish_source=config["networks"][network.show_active()].get("verify", False)
    creation_transaction.wait(1)
    print("Donkey Warrior Created!")
    