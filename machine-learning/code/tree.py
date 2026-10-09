"""A small decision tree, for lessons 4 and 6. Pure Python. Built to be read, not to be fast."""


def gini(labels):
    """Impurity: 0 when every row has the same label, 0.5 when it is an even mix."""
    if not labels:
        return 0.0
    p = sum(labels) / len(labels)
    return 2 * p * (1 - p)


def grow(rows, labels, max_depth, min_leaf=5, depth=0):
    """Split the rows on the single question (feature <= cut) that makes the groups purest.

    Repeat inside each group until max_depth or the group is small. A leaf stores the share of
    churners in its group. Returns a nested dict.
    """
    leaf = {"p": sum(labels) / len(labels), "n": len(labels)}
    if depth >= max_depth or len(labels) < 2 * min_leaf or gini(labels) == 0.0:
        return leaf
    best = None
    n, total_pos = len(labels), sum(labels)
    for f in range(len(rows[0])):
        ordered = sorted(zip((r[f] for r in rows), labels))      # sort once, then sweep the cut point
        left_n = left_pos = 0
        for i in range(n - 1):
            left_n += 1
            left_pos += ordered[i][1]
            if ordered[i][0] == ordered[i + 1][0]:
                continue                                         # cannot cut between equal values
            right_n, right_pos = n - left_n, total_pos - left_pos
            if left_n < min_leaf or right_n < min_leaf:
                continue
            pl, pr = left_pos / left_n, right_pos / right_n
            score = (left_n * 2 * pl * (1 - pl) + right_n * 2 * pr * (1 - pr)) / n
            if best is None or score < best[0]:
                best = (score, f, (ordered[i][0] + ordered[i + 1][0]) / 2)
    if best is None:
        return leaf
    _, f, cut = best
    go_left = [r[f] <= cut for r in rows]
    return {
        "f": f, "cut": cut,
        "left": grow([r for r, g in zip(rows, go_left) if g], [y for y, g in zip(labels, go_left) if g],
                     max_depth, min_leaf, depth + 1),
        "right": grow([r for r, g in zip(rows, go_left) if not g], [y for y, g in zip(labels, go_left) if not g],
                      max_depth, min_leaf, depth + 1),
    }


def proba(tree, row):
    while "f" in tree:
        tree = tree["left"] if row[tree["f"]] <= tree["cut"] else tree["right"]
    return tree["p"]


def depth_of(tree):
    return 0 if "f" not in tree else 1 + max(depth_of(tree["left"]), depth_of(tree["right"]))
