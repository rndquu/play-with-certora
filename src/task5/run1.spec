methods {
    function count() external returns (uint) envfree;
}
invariant countNot3()
    count() != 3;

// rule canNotBe3(method f1, method f2) {
//     require count() == 0;

//     env e;
//     calldataarg args;
//     f1(e, args);

//     env e2;
//     calldataarg args2;
//     f2(e2, args2);

//     assert count() != 3;
// }
