from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link
from brownie import BattleDonkeyz, config, network


def deploy_and_create():
    account = get_account()
    donkey_warrior = BattleDonkeyz.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    fund_with_link(donkey_warrior.address)
    creating_tx = donkey_warrior.createDonkey({"from": account})
    creating_tx.wait(1)
    print("New token has been created")
    return donkey_warrior, creating_tx


def main():
    deploy_and_create()