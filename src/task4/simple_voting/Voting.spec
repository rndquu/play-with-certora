methods {
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;
}

// sum of votes in favor and against == total number of voted
// NOTICE: also checks that invariant holds after constructor
invariant sumResultsEqualsTotalVotes()
    votesInFavor() + votesAgainst() == to_mathint(totalVotes());

// correct translation of the invariant
rule sumResultsEqualsTotalVotesAsRule(method f) {
    // precondition
    require votesInFavor() + votesAgainst() == to_mathint(totalVotes());

    // call all methods except constructor
    env e;
    calldataarg args;
    f(e, args);

    assert (
        votesInFavor() + votesAgainst() == to_mathint(totalVotes()), 
        "Sum of votes should equal total votes"
    );
}    

// wrong translation of the invariant (no preconditions)
rule sumResultsEqualsTotalVotesWrong() {
    assert (
        votesInFavor() + votesAgainst() == to_mathint(totalVotes()), 
        "Sum of votes should equal total votes"
    );
}    
