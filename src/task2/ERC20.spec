methods {
    // when function is not using the environment (i.e. `msg.sender`) it can be
    // declared as `envfree`
    function balanceOf(address) external returns (uint) envfree;
    function allowance(address, address) external returns (uint) envfree;
    function totalSupply() external returns (uint) envfree;
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