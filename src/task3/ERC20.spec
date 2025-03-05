methods {
    // when function is not using the environment (i.e. `msg.sender`) it can be
    // declared as `envfree`
    function totalSupply() external returns (uint) envfree;
    function balanceOf(address) external returns (uint) envfree;
    function allowance(address, address) external returns (uint) envfree;
    function _owner() external returns (address) envfree;
}

// check that `transferFrom()` decreases allowance of `e.msg.sender`
rule integrityOfTransferFrom(address sender, address recipient, uint256 amount) {
    env e;

    require sender != recipient;
    require amount != 0;

    uint256 allowanceBefore = allowance(sender, e.msg.sender);
    transferFrom(e, sender, recipient, amount);
    uint256 allowanceAfter = allowance(sender, e.msg.sender);

    assert 
        allowanceBefore > allowanceAfter, 
        "Allowance must decrease after using allowance to pay on behalf of somebody else";
}

function callFunctionWithParams(env e, method f, address from, address to) {
    uint256 amount;

    if (f.selector == sig:transfer(address, uint256).selector) {
        require e.msg.sender == from;
        transfer(e, to, amount);
    } else if (f.selector == sig:allowance(address, address).selector) {
        allowance(e, from, to);
    } else if (f.selector == sig:approve(address, uint256).selector) {
        approve(e, to, amount);
    } else if (f.selector == sig:transferFrom(address, address, uint256).selector) {
        transferFrom(e, from, to, amount);
    } else if (f.selector == sig:increaseAllowance(address, uint256).selector) {
        increaseAllowance(e, to, amount);
    } else if (f.selector == sig:decreaseAllowance(address, uint256).selector) {
        decreaseAllowance(e, to, amount);
    } else if (f.selector == sig:mint(address, uint256).selector) {
        mint(e, to, amount);
    } else if (f.selector == sig:burn(address, uint256).selector) {
        burn(e, from, amount);
    } else {
        calldataarg args;
        f(e, args);
    }
}

/** User's balance can only be changed as a result of:
    - `transfer()`
    - `transferFrom()`
    - `mint()`
    - `burn()`
*/
rule balanceChangesFromCertainFunctions(method f, address user) {
    env e;
    calldataarg args;

    uint256 userBalanceBefore = balanceOf(user);
    f(e, args);
    uint256 userBalanceAfter = balanceOf(user);

    assert
        userBalanceAfter != userBalanceBefore => (
            f.selector == sig:transfer(address, uint256).selector ||
            f.selector == sig:transferFrom(address, address, uint256).selector ||
            f.selector == sig:mint(address, uint256).selector ||
            f.selector == sig:burn(address, uint256).selector
        ),
        "User's balance changed not from `transfer()`, `transferFrom()`, `mint()`, `burn()`";
}

rule onlyOwnersMayChangeTotalSupply(method f) {
    env e;

    uint256 totalSupplyBefore = totalSupply();
    calldataarg args;
    f(e, args);
    uint256 totalSupplyAfter = totalSupply();

    assert totalSupplyAfter != totalSupplyBefore => e.msg.sender == _owner();
}

/*
    Given addresses:
    - e.msg.sender
    - from
    - to
    - thirdParty
    we check that there is no method `f()` that would:
    1) Not take `thirdParty` as an input argument and
    2) yet changed the balance of `thirdParty`
    Simply put we target the case from a transfer of tokens `from` -> `to`
    changes the balance of `thirdParty`.
*/
rule doesNotAffectAThirdPartyBalance(method f) {
    env e;
    address from;
    address to;
    address thirdParty;

    require (thirdParty != from) && (thirdParty != to);

    uint thirdPartyBalanceBefore = balanceOf(thirdParty);
    callFunctionWithParams(e, f, from, to);
    uint thirdPartyBalanceAfter = balanceOf(thirdParty);

    assert 
        thirdPartyBalanceAfter == thirdPartyBalanceBefore, 
        "`thirdParty` balance unexpectedly modified";
}
