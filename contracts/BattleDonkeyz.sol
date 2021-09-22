// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract BattleDonkeyz is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Donkey {
        JETHRO,
        REBEL,
        ROSCOE,
        TWEAK,
        BUSTA
    }
    mapping(uint256 => Donkey) public tokenIdToDonkey;
    mapping(bytes32 => address) public requestIdToSender;

    event requestedDonkey(bytes32 indexed requestId, address requester);
    event donkeyNamed(uint256 indexed tokenId, Donkey name);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Battle Donkeys", "DONK")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createDonkey() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedDonkey(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Donkey name = Donkey(randomNumber % 5);
        uint256 newTokenId = tokenCounter;
        tokenIdToDonkey[newTokenId] = name;
        address owner = requestIdToSender[requestId];
        emit donkeyNamed(newTokenId, name);
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner or approved!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
