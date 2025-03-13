// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {Counter} from "../../src/task5/Counter.sol";

contract CounterTest is Test {
    Counter counter;

    function setUp() public {
        counter = new Counter();
    }

    // function test_increment() public {
    //     assertEq(counter.count(), 0);
    //     counter.increment();
    //     assertEq(counter.count(), 1);
    // }
}
