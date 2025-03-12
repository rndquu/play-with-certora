/**
 * # Spec for funds manager `IManager.sol`
 */
methods {
    function getCurrentManager(uint256) external returns (address) envfree;
    function getPendingManager(uint256) external returns (address) envfree;
    function isActiveManager(address) external returns (bool) envfree;
}

// Inverse mapping from managers to fund ids
ghost mapping(address => uint256) managerFunds;

hook Sstore funds[KEY uint256 fundId].(offset 0) address newManager {
    managerFunds[newManager] = fundId;
}

// Address zero is never an active manager
invariant zeroIsNeverActive()
    !isActiveManager(0);

// Every active manager has a fund they manage
invariant activeManagesAFund(address manager)
    isActiveManager(manager) => getCurrentManager(managerFunds[manager]) == manager
    {
        preserved {
            requireInvariant zeroIsNeverActive();
        }
    }
