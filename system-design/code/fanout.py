"""News feed: cost of fan-out on write vs fan-out on read, and the hybrid. Run: python3 fanout.py"""

# (followers, posts per day) for a few kinds of account. Numbers are invented.
ACCOUNTS = [("regular", 200, 2)] * 99_000 + [("popular", 50_000, 3)] * 900 + [("celebrity", 20_000_000, 5)] * 100
READS_PER_USER_PER_DAY = 30
FOLLOWEES_PER_READ = 200
CELEBRITIES_FOLLOWED = 5     # a reader merges in the posts of a handful of celebrities at read time


def push_cost(accounts):
    """Feed-cache writes per day: every post is copied into every follower's feed."""
    return sum(f * p for _, f, p in accounts)


def pull_cost(users):
    """Post lookups per day: every feed read merges the posts of every followee."""
    return users * READS_PER_USER_PER_DAY * FOLLOWEES_PER_READ


def hybrid_cost(accounts, users, threshold=1_000_000):
    pushed = sum(f * p for _, f, p in accounts if f < threshold)
    pulled = users * READS_PER_USER_PER_DAY * CELEBRITIES_FOLLOWED
    return pushed + pulled


if __name__ == "__main__":
    users = 10_000_000
    push, pull, hybrid = push_cost(ACCOUNTS), pull_cost(users), hybrid_cost(ACCOUNTS, users)
    celeb_share = sum(f * p for _, f, p in ACCOUNTS if f >= 1_000_000) / push
    print(f"push: {push:,.0f} writes/day, {celeb_share:.0%} of them for 100 celebrity accounts")
    print(f"pull: {pull:,.0f} lookups/day")
    print(f"hybrid: {hybrid:,.0f} operations/day")
    assert celeb_share > 0.97 and hybrid < push / 5 and hybrid < pull / 30
    print("fanout ok")
