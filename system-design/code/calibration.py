"""Ads: ranking quality is not enough, because auctions use the predicted click probability as a price.
Two models rank ads identically, and one is miscalibrated. Run: python3 calibration.py"""

ADS = [  # (name, bid in dollars per click, true click probability)
    ("a", 2.00, 0.010), ("b", 1.00, 0.030), ("c", 0.50, 0.050), ("d", 3.00, 0.005),
]


def expected_revenue_rank(pctr):
    return sorted(ADS, key=lambda ad: -ad[1] * pctr[ad[0]])


def calibration_ratio(pctr, impressions=1000):
    predicted = sum(pctr[n] for n, _, _ in ADS) * impressions
    actual = sum(p for _, _, p in ADS) * impressions
    return predicted / actual


if __name__ == "__main__":
    true = {n: p for n, _, p in ADS}
    inflated = {n: 3 * p for n, _, p in ADS}                    # same ordering by probability, three times too high
    skewed = {"a": 0.020, "b": 0.030, "c": 0.050, "d": 0.005}   # distorts only one ad's probability
    order_true = [a[0] for a in expected_revenue_rank(true)]
    order_inflated = [a[0] for a in expected_revenue_rank(inflated)]
    order_skewed = [a[0] for a in expected_revenue_rank(skewed)]
    print(f"auction order with true probabilities {order_true}; with probabilities 3x too high {order_inflated}; with one ad over-estimated {order_skewed}")
    print(f"predicted clicks / actual clicks: true {calibration_ratio(true):.2f}, inflated {calibration_ratio(inflated):.2f}, skewed {calibration_ratio(skewed):.2f}")
    # an advertiser billed per click pays bid per click; expected-value pricing for an impression is bid * pCTR
    price_true = ADS[0][1] * true["a"]
    price_inflated = ADS[0][1] * inflated["a"]
    print(f"an impression of ad a is worth ${price_true:.3f} with the true probability and ${price_inflated:.3f} with an inflated one")
    assert order_true == order_inflated                          # scaling does not change the order
    assert order_skewed != order_true
    assert abs(calibration_ratio(inflated) - 3) < 1e-9 and abs(calibration_ratio(true) - 1) < 1e-9
    assert abs(price_inflated / price_true - 3) < 1e-9
    print("calibration ok")
