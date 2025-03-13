// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.28;

contract Counter {
    uint public count;

    // function increment() public {
    //     count++;
    // }

    function increaseBy1() public {
        count += 1;
    }

    function increaseBy2() public {
        count += 2;
    }
}
