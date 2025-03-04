methods {
    function amounts(address) external returns (uint256) envfree;
    function maximalAmount() external returns (uint256) envfree;
    function add(address, uint256) external returns (uint256) envfree;
    function sub(address, uint256) external returns (uint256) envfree;
}

rule simpleVacuousRule(uint256 x, uint256 y) {
    // contradictory requirement
    require (x > y) && (y > x);
    assert false; // should always fail
}

rule subtleVacuousRule(address user, uint256 amount) {
    uint256 userAmount = amounts(user);
    require amount > userAmount;
    sub(user, amount); // always reverts, no computation paths => vacuous
    assert false; // should always fail
}

rule revertingRule(address user, uint256 amount) {
    uint256 userAmount = amounts(user);
    require amount > userAmount;
    sub@withrevert(user, amount); // always reverts, computation paths exist since `withrevert` is used
    assert lastReverted; // `true` if the last solidity function called reverted
}
