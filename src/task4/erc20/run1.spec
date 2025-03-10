methods {
    function balanceOf(address) external returns (uint256) envfree;
}

// Zero address has no balance
invariant zeroHasNoBalance()
    balanceOf(0) == 0;
