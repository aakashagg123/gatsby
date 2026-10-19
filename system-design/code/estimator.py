"""Back-of-envelope helpers for the numbers-and-formulas and foundations lessons.
Every figure is an estimate. Run: python3 estimator.py
"""
SECONDS_PER_DAY = 86_400
BASE62 = 62


def per_second(per_day):
    return per_day / SECONDS_PER_DAY


def twitter_like(dau=200e6, posts_per_user=2, read_ratio=100, bytes_per_post=300):
    posts = dau * posts_per_user
    write_qps = per_second(posts)
    return dict(write_qps=write_qps, peak_write_qps=3 * write_qps, read_qps=write_qps * read_ratio,
                gb_per_day=posts * bytes_per_post / 1e9, tb_per_year=posts * bytes_per_post * 365 / 1e12)


def base62_space(chars):
    return BASE62 ** chars


def years_of_codes(chars, new_links_per_day):
    return base62_space(chars) / new_links_per_day / 365


def downtime_minutes(availability, days=30):
    return (1 - availability) * days * 24 * 60


def series(*avail):
    out = 1.0
    for a in avail:
        out *= a
    return out


def parallel(*avail):
    out = 1.0
    for a in avail:
        out *= (1 - a)
    return 1 - out


def vector_memory_tb(vectors, dims=128, bytes_per_number=4):
    return vectors * dims * bytes_per_number / 1e12


if __name__ == "__main__":
    t = twitter_like()
    print(f"write {t['write_qps']:,.0f}/s (peak {t['peak_write_qps']:,.0f}), read {t['read_qps']:,.0f}/s, "
          f"{t['gb_per_day']:.0f} GB/day, {t['tb_per_year']:.1f} TB/year")
    print(f"base62: 6 chars {base62_space(6):.3g}, 7 chars {base62_space(7):.3g}; 7 chars at 100M links/day last {years_of_codes(7, 100e6):.0f} years")
    for a in (0.99, 0.999, 0.9999, 0.99999):
        print(f"{a:.3%} -> {downtime_minutes(a):.2f} minutes per 30 days, {downtime_minutes(a, 365.25) / 60:.2f} hours per year")
    print(f"two 99.9% in series {series(.999, .999):.5f}; in parallel {parallel(.999, .999):.6f}")
    print(f"100B vectors x 128 dims x 4 bytes = {vector_memory_tb(100e9):.1f} TB; at 32 bytes each {100e9 * 32 / 1e12:.1f} TB")
    assert round(t["write_qps"]) == 4630 and round(t["read_qps"]) == 462_963
    assert round(t["gb_per_day"]) == 120 and round(t["tb_per_year"], 1) == 43.8
    assert round(base62_space(6) / 1e9, 1) == 56.8 and round(base62_space(7) / 1e12, 2) == 3.52
    assert round(years_of_codes(7, 100e6)) == 96
    assert round(downtime_minutes(0.999), 1) == 43.2 and round(downtime_minutes(0.9999), 2) == 4.32
    assert round(series(.999, .999), 5) == 0.99800 and round(parallel(.999, .999), 6) == 0.999999
    assert round(vector_memory_tb(100e9), 1) == 51.2
    print("estimator ok")
