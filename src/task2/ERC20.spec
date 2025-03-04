methods {
    // when function is not using the environment (i.e. `msg.sender`) it can be
    // declared as `envfree`
    function balanceOf(address) external returns (uint) envfree;
    function allowance(address, address) external returns (uint) envfree;
    function totalSupply() external returns (uint) envfree;
}

rule onlyHolderCanChangeAllowance(address holder, address spender, method f) {
    // allowance before the method was called
    mathint allowance_before = allowance(holder, spender);

    env e;
    calldataarg args; // arguments for the method `f()`
    f(e, args);

    // allowance after the method was called
    mathint allowance_after = allowance(holder, spender);

    assert allowance_after > allowance_before => e.msg.sender == holder,
        "Only the sender can change its own allowance";

    // assert that if the allowance was changed then `approve()` or 
    // `increaseAllowance()` was called
    assert(
        allowance_after > allowance_before => (
            f.selector == sig:approve(address, uint).selector ||
            f.selector == sig:increaseAllowance(address, uint).selector
        )
    ),
    "Only `approve()` and `increaseAllowance()` can increase allowances";
}


rule totalSupplyAfterMintWithPrecondition(address account, uint256 amount) {
    env e;

    // Assume that in the current state, before minting,
    // total supply of tokens >= user's balance
    uint256 userBalanceBefore = balanceOf(account);
    uint256 totalBefore = totalSupply();
    require totalBefore >= userBalanceBefore;

    mint(e, account, amount);

    uint256 userBalanceAfter = balanceOf(account);
    uint256 totalAfter = totalSupply();

    assert totalAfter >= userBalanceAfter, "Total supply is less than a single user's balance";
}

// Total supply after mint is at least the balance of the receiving account
rule totalSupplyAfterMint(address account, uint256 amount) {
    env e;

    uint256 userBalanceBefore = balanceOf(account);
    uint256 totalBefore = totalSupply();

    mint(e, account, amount);

    uint256 userBalanceAfter = balanceOf(account);
    uint256 totalAfter = totalSupply();

    assert totalAfter >= userBalanceAfter, "Total supply is less than a single user's balance";
}

rule transferSpec(address recipient, uint amount) {
    env e;

    // `mathint` => integer type of any size
    mathint balance_sender_before = balanceOf(e.msg.sender);
    mathint balance_recipient_before = balanceOf(recipient);

    transfer(e, recipient, amount);

    mathint balance_sender_after = balanceOf(e.msg.sender);
    mathint balance_recipient_after = balanceOf(recipient);

    // `mathint` can never underflow and overflow
    assert e.msg.sender != recipient => balance_sender_after == balance_sender_before - amount, "sender's balance must be decreased";
    assert e.msg.sender != recipient => balance_recipient_after == balance_recipient_before + amount, "recipient's balance must be increased";
    assert e.msg.sender == recipient => balance_sender_after == balance_recipient_after, "self transfer is allowed";
}

/* Flawed: allows self transder
rule transferSpec(address recipient, uint amount) {
    env e;

    // `mathint` => integer type of any size
    mathint balance_sender_before = balanceOf(e.msg.sender);
    mathint balance_recipient_before = balanceOf(recipient);

    transfer(e, recipient, amount);

    mathint balance_sender_after = balanceOf(e.msg.sender);
    mathint balance_recipient_after = balanceOf(recipient);

    // `mathint` can never underflow and overflow
    assert balance_sender_after == balance_sender_before - amount, "sender's balance must be decreased";
    assert balance_recipient_after == balance_recipient_before + amount, "recipient's balance must be increased";
}
*/