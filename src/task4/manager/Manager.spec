/**
 * # Spec for funds manager `IManager.sol`
 */
methods {
    function getCurrentManager(uint256) external returns (address) envfree;
    function getPendingManager(uint256) external returns (address) envfree;
    function isActiveManager(address) external returns (bool) envfree;
}

// function isManaged(uint256 fundId) returns bool {
//     return getCurrentManager(fundId) != 0;
// }

// Fund's manager is active
invariant managerIsActive(uint256 fundId)
    (getCurrentManager(fundId) != 0) => isActiveManager(getCurrentManager(fundId))
    {
        preserved claimManagement(uint256 fundId2) with (env e) {
            requireInvariant uniqueManager(fundId, fundId2);
        }
    }

// Fund has a unique manager
invariant uniqueManager(uint256 fundId1, uint256 fundId2)
    ((fundId1 != fundId2) && (getCurrentManager(fundId1) != 0)) => (
        getCurrentManager(fundId1) != getCurrentManager(fundId2)
    ) {
        preserved {
            requireInvariant managerIsActive(fundId1);
            requireInvariant managerIsActive(fundId2);
        }
    }
