from brownie import network, BattleDonkeyz
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.donkey_battle.deploy_and_create_donkey import deploy_and_create

def test_can_create_donkey():
  # Deploy Contract
  # Create a random Donkey
  # get a random named donkey back
  
  # Arrange
  if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    pytest.skip("Only for local testing")

  # Act
  donkey_battle, creating_tx = deploy_and_create()
  requestId = creating_tx.events["requestedDonkey"]["requestId"]
  random_number = 777 
  
  get_contract("vrf_coordinator").callBackWithRandomness(requestId, random_number, donkey_battle.address, {"from": get_account()})
  
  # Assert
  assert donkey_battle.tokenCounter() == 1
  assert donkey_battle.tokenIdToDonkey(0) == random_number % 5
  
  
  