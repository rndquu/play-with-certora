methods {
    function highestBidder() external returns (address) envfree;
    function highestBid() external returns (uint) envfree;
    function bids(address) external returns (uint) envfree;
}

// `highestBid` is the max bid
invariant integrityOfHighestBid(address bidder)
    highestBid() >= bids(bidder);

invariant highestBidderHasHighestBid()
    highestBidder() != 0 => bids(highestBidder()) == highestBid();

