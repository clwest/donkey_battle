pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract BattleStats is ERC721, VRFConsumerBase, Ownable {
    using SafeMath for uint256;
    using Strings for string;

    uint256 public tokenCounter;
    bytes32 internal keyHash;
    uint256 public fee;
    //uint256 public randomNumber;
    // Rinkeby Network
    address public VRFCoordinator;
    address public LinkToken;

    struct Donkey {
        uint256 stubborness;
        uint256 skinToughness;
        uint256 kick;
        uint256 bite;
        uint256 whinny;
        uint256 donkeyPunch;
        uint256 experience;
        string name;
        // TODO: Add more!
    }

    Donkey[] public donkeyz;

    mapping(bytes32 => string) requestDonkeyName;
    mapping(bytes32 => address) requestToSender;
    mapping(bytes32 => uint256) requestToTokenId;

    constructor(
        address _VRFCoordinator,
        address _LinkToken,
        bytes32 _keyhash
    )
        public
        VRFConsumerBase(_VRFCoordinator, _LinkToken)
        ERC721("DonkeyBetz", "DONK")
    {
        VRFCoordinator = _VRFCoordinator;
        LinkToken = _LinkToken;
        keyHash = _keyhash;
        fee = 0.1 * 10**18;
        tokenCounter = 0;
    }

    function createDonkey(string memory name, uint256 tokenURI)
        public
        returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestDonkeyName[requestId] = name;
        requestToSender[requestId] = msg.sender;
        return requestId;
    }

    function getTokenURI(uint256 tokenId) public view returns (string memory) {
        return tokenURI(tokenId);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        uint256 newId = donkeyz.length;
        uint256 stubborness = (randomNumber % 100);
        uint256 skinToughness = ((randomNumber % 10000) / 100);
        uint256 kick = ((randomNumber % 1000000) / 10000);
        uint256 bite = ((randomNumber % 10000000) / 1000000);
        uint256 whinny = ((randomNumber % 10000000000) / 100000000);
        uint256 donkeyPunch = ((randomNumber % 1000000000000) / 10000000000);
        uint256 experience = 0;

        donkeyz.push(
            Donkey(
                stubborness,
                skinToughness,
                kick,
                bite,
                whinny,
                donkeyPunch,
                experience,
                requestDonkeyName[requestId]
            )
        );

        _safeMint(requestToSender[requestId], newId);
        tokenCounter = tokenCounter + 1;
    }

    function getLevel(uint256 tokenId) public view returns (uint256) {
        return sqrt(donkeyz[tokenId].experience);
    }

    function getNumberOfDonkeyz() public view returns (uint256) {
        return donkeyz.length;
    }

    function getDonkeyOverView(uint256 tokenId)
        public
        view
        returns (
            string memory,
            uint256,
            uint256,
            uint256
        )
    {
        return (
            donkeyz[tokenId].name,
            donkeyz[tokenId].stubborness +
                donkeyz[tokenId].skinToughness +
                donkeyz[tokenId].kick +
                donkeyz[tokenId].bite +
                donkeyz[tokenId].whinny +
                donkeyz[tokenId].donkeyPunch,
            getLevel(tokenId),
            donkeyz[tokenId].experience
        );
    }

    function getDonkeyStats(uint256 tokenId)
        public
        view
        returns (
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256,
            uint256
        )
    {
        return (
            donkeyz[tokenId].stubborness,
            donkeyz[tokenId].skinToughness,
            donkeyz[tokenId].kick,
            donkeyz[tokenId].bite,
            donkeyz[tokenId].whinny,
            donkeyz[tokenId].donkeyPunch,
            donkeyz[tokenId].experience
        );
    }

    function sqrt(uint256 x) internal view returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
}
