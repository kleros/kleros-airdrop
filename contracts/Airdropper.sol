pragma solidity ^0.4.15;

import "https://github.com/OpenZeppelin/zeppelin-solidity/contracts/ownership/Ownable.sol";
import "https://github.com/OpenZeppelin/zeppelin-solidity/contracts/token/ERC20/ERC20.sol";

contract Airdropper is Ownable {
    ERC20 tokenContract;

    function Airdropper(ERC20 _tokenContract) public Ownable() {
        tokenContract = _tokenContract;
    }

    /** Transfer ERC20 compatible token to recipeients of airdrop. The index of each recipient should
     *  have a cooresponding value in _values. Note that this is O(n) so trying to
     *  airdrop to too many recipients in one shot may exceed gas limit.
     *  @param _recipients The array of recipient addresses
     *  @param _values The amount of PNK to send to recipeient i
     */
    function airdropTokens(address[] _recipients, uint[] _values) public onlyOwner {
        for (uint i = 0; i < _recipients.length; i++) {
            tokenContract.transfer(_recipients[i], _values[i]);
        }
    }

}
