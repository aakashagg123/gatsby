"""Tiered photo storage: keep hot data with many full copies, and warm data erasure-coded. Storage is logical size times the
effective replication factor. The 3.6x and 2.1x factors are the ones the f4 paper's abstract reports for warm data before and after. Run: python3 photo_tiers.py"""


def physical(logical_pb, factor):
    return logical_pb * factor


def blended(hot_pb, warm_pb, hot_factor, warm_factor):
    return physical(hot_pb, hot_factor) + physical(warm_pb, warm_factor)


if __name__ == "__main__":
    logical = 65.0                                   # petabytes of logical data, the f4 abstract's figure for warm data
    all_hot = physical(logical, 3.6)
    all_warm = physical(logical, 2.1)
    print(f"{logical:.0f} PB of warm data: {all_hot:.0f} PB at a 3.6x factor, {all_warm:.1f} PB at 2.1x, saving {all_hot - all_warm:.1f} PB")
    mix = blended(hot_pb=10, warm_pb=90, hot_factor=3.6, warm_factor=2.1)
    flat = physical(100, 3.6)
    print(f"100 PB with 10% hot and 90% warm: {mix:.0f} PB tiered against {flat:.0f} PB without tiers ({1 - mix / flat:.0%} less)")
    assert round(all_hot) == 234 and round(all_warm, 1) == 136.5
    assert round(mix) == 225 and flat == 360.0
    print("photo tiers ok")
