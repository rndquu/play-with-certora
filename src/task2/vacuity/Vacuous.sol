// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Vacuous {
    mapping (address => uint256) public amounts;
    uint256 public immutable maximalAmount = 1000;

    function add(address user, uint256 amount) public returns (uint256) {
        require(amounts[user] + amount <= maximalAmount);
        amounts[user] += amount;
        return amounts[user];
    }

    function sub(address user, uint256 amount) public returns (uint256) {
        amounts[user] -= amount;
        return amounts[user];
    }
}
