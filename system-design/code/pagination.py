"""Offset pagination skips or repeats rows when data changes; a cursor does not. Run: python3 pagination.py"""


def page_offset(rows, offset, size):
    return rows[offset:offset + size]


def page_cursor(rows, after_id, size):
    return [r for r in rows if r > after_id][:size]


if __name__ == "__main__":
    # a feed sorted by id descending is awkward; use ascending ids and let new rows arrive at the front of a newest-first list
    rows = list(range(100, 0, -1))                 # newest first: 100, 99, ..., 1
    first = page_offset(rows, 0, 10)               # 100..91
    rows = [101, 102] + rows                       # two new rows arrive while the user reads
    second = page_offset(rows, 10, 10)             # offset 10 now starts two rows earlier
    repeated = set(first) & set(second)

    rows = list(range(100, 0, -1))
    first_c = rows[:10]
    cursor = first_c[-1]
    rows = [101, 102] + rows
    second_c = [r for r in rows if r < cursor][:10]
    print(f"offset paging after 2 new rows: page 2 repeats {sorted(repeated, reverse=True)}; cursor paging repeats {sorted(set(first_c) & set(second_c))}")
    assert len(repeated) == 2 and not (set(first_c) & set(second_c))
    assert second_c == list(range(90, 80, -1))
    print("pagination ok")
