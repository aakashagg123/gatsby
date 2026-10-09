"""Lesson 4: a model can memorize its training rows. Two charts tell you when it has.

Chart 1 (complexity): deeper decision trees fit the training rows better and unseen rows worse.
Chart 2 (learning curve): with more training rows, the gap between the two scores closes.

Run: python3 lesson4_overfitting.py
"""
from data import make_customers
from lesson1_rules_vs_learning import balanced_accuracy
from tree import depth_of, grow, proba


def scores(tree, cut, train, test):
    f = lambda rows: [1 if proba(tree, x) >= cut else 0 for x in rows]
    return balanced_accuracy(f(train[0]), train[1]), balanced_accuracy(f(test[0]), test[1])


def main():
    rows, labels = make_customers(6000)
    valid = (rows[3000:4500], labels[3000:4500])   # used to choose the depth
    test = (rows[4500:], labels[4500:])            # looked at once, at the end

    # Chart 1: fix the training set at 600 rows and let the tree get deeper.
    train = (rows[:600], labels[:600])
    cut = sum(train[1]) / len(train[1])
    complexity = {}
    for depth in (1, 2, 3, 4, 6, 8, 12):
        tree = grow(train[0], train[1], depth, min_leaf=1)
        complexity[depth] = scores(tree, cut, train, valid)

    # Chart 2: fix the tree at depth 8 and give it more and more rows.
    curve = {}
    for n in (50, 100, 200, 400, 800, 1600, 3000):
        tr = (rows[:n], labels[:n])
        tree = grow(tr[0], tr[1], 8, min_leaf=1)
        curve[n] = scores(tree, sum(tr[1]) / n, tr, valid)

    # Choose the depth on the validation rows. Only then look at the test rows.
    best_depth = max(complexity, key=lambda d: complexity[d][1])
    tree = grow(train[0], train[1], best_depth, min_leaf=1)
    final = scores(tree, cut, train, test)[1]
    return complexity, curve, best_depth, final


if __name__ == "__main__":
    complexity, curve, best_depth, final = main()
    print("depth  train  valid")
    for d, (a, b) in complexity.items():
        print(f"{d:5d}  {a:.3f}  {b:.3f}")
    print("rows   train  valid  gap")
    for n, (a, b) in curve.items():
        print(f"{n:5d}  {a:.3f}  {b:.3f}  {a - b:.3f}")
    print(f"best depth on the validation rows: {best_depth}; score on the untouched test rows: {final:.3f}")
    assert complexity[12][0] > 0.9                      # the deep tree nearly memorizes the 600 rows
    assert complexity[12][1] < complexity[4][1]         # and does worse on rows it has not seen
    assert best_depth in (3, 4, 6)
    assert abs(final - complexity[best_depth][1]) < 0.05    # the test rows agree with validation
    assert curve[50][0] - curve[50][1] > curve[3000][0] - curve[3000][1]   # the gap closes
    assert curve[3000][1] > curve[50][1]
    print("lesson 4 ok")
