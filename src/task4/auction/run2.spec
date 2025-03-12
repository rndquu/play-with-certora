methods {
    function highestBidder() external returns (address) envfree;
    function highestBid() external returns (uint) envfree;
    function bids(address) external returns (uint) envfree;
}

// A ghost and hook identifying if any bid was placed
ghost bool _hasAnyoneBid {
    init_state axiom !_hasAnyoneBid;
}

hook Sstore bids[KEY address bidder] uint newAmount (uint oldAmount) {
    _hasAnyoneBid = _hasAnyoneBid || (newAmount > 0);
}

// `highestBid` is the max bid
invariant integrityOfHighestBid(address bidder)
    highestBid() >= bids(bidder);

// No bids implies all bids are 0 and highest bidder is address(0)
invariant noBidsIntegrity(address bidder)
    !_hasAnyoneBid => (bids(bidder) == 0 && highestBidder() == 0);

// There can be no tie in highest bid (if there is at least one bid)
invariant highestBidStrictlyHighest(address bidder)
    (_hasAnyoneBid && bidder != highestBidder()) => (highestBid() > bids(bidder)) {
        preserved {
            requireInvariant integrityOfHighestBid(bidder);
        }
        preserved withdrawFor(address bidder2, uint amount) with (env e1) {
            requireInvariant noBidsIntegrity(bidder2);
        }
        preserved withdrawAmount(address recipient, uint amount) with (env e2) {
            requireInvariant noBidsIntegrity(e2.msg.sender);
        }
    }

// Invariant "highest bidder has the highest bid" without assuming
// that `address(0)` cannot place a bid
invariant highestBidderHasHighestBid()
    _hasAnyoneBid => (bids(highestBidder()) == highestBid()) {
        preserved withdrawFor(address bidder2, uint amount) with (env e1) {
            requireInvariant noBidsIntegrity(bidder2);
        }
        preserved withdrawAmount(address recipient, uint amount) with (env e2) {
            requireInvariant noBidsIntegrity(e2.msg.sender);
        }
    }
