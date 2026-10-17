"""Lesson 5: the dataset. An audit that finds duplicates, conflicts, leaks and outliers before training.

The examples are invented, with known problems planted in them. Run: python3 lesson5_dataset.py
"""
import statistics

TRAIN = [
    ("How do I reset my password?", "Go to Settings, choose Security, then Reset password."),
    ("How do I reset my password?", "Go to Settings, choose Security, then Reset password."),               # exact duplicate
    ("how do i reset my password", "Go to Settings, choose Security, then Reset password."),               # near duplicate
    ("Can I get a refund on an annual plan?", "Yes, within 14 days of purchase."),
    ("Can I get a refund on an annual plan?", "No, annual plans are not refundable."),                     # conflicting answer
    ("What does error E-4021 mean?", "The bank feed timed out. Reconnect the bank in Settings."),
    ("How do I export my invoices?", "Use Settings, then Export, and choose CSV."),
    ("Where is my data stored?", "EU workspaces are stored in Frankfurt. Others are stored in Virginia."),
    ("What is the API rate limit?", "600 requests per minute for each workspace."),
    ("How do I add a client?", "Choose New client, then enter the name and email address."),
    ("Is there a free plan?", ""),                                                                          # empty answer
    ("Summarize my account", "x " * 400),                                                                   # length outlier
    ("How do I cancel my plan?", "Go to Settings, choose Billing, then End plan."),
    ("Can I invite a teammate?", "Yes. Team plans include up to 10 users."),
]
EVAL = [
    ("What does error E-4021 mean?", "The bank feed timed out."),                                            # also in TRAIN: a leak
    ("Can I change my invoice template?", "Yes, under Settings, then Templates."),
]


def normalize(text):
    return " ".join("".join(c.lower() if c.isalnum() else " " for c in text).split())


def shingles(text, k=3):
    words = normalize(text).split()
    return {tuple(words[i:i + k]) for i in range(max(1, len(words) - k + 1))}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def audit(train, evalset):
    found = dict(exact=[], near=[], conflicts=[], empty=[], long=[], leaks=[])
    seen = {}
    for i, (q, a) in enumerate(train):
        if not a.strip():
            found["empty"].append(i)
        if (q, a) in seen:
            found["exact"].append(i)
        seen.setdefault((q, a), i)
    pairs = [(i, j) for i in range(len(train)) for j in range(i + 1, len(train))]
    for i, j in pairs:
        (q1, a1), (q2, a2) = train[i], train[j]
        if (q1, a1) == (q2, a2):
            continue
        if jaccard(shingles(q1 + " " + a1), shingles(q2 + " " + a2)) >= 0.8:
            found["near"].append((i, j))
        elif normalize(q1) == normalize(q2) and normalize(a1) != normalize(a2):
            found["conflicts"].append((i, j))
    lengths = [len(a) for _, a in train]
    mean, sd = statistics.mean(lengths), statistics.pstdev(lengths)
    found["long"] = [i for i, n in enumerate(lengths) if sd and (n - mean) / sd > 2.5]
    train_q = {normalize(q) for q, _ in train}
    found["leaks"] = [k for k, (q, _) in enumerate(evalset) if normalize(q) in train_q]
    return found


def main():
    return audit(TRAIN, EVAL)


if __name__ == "__main__":
    f = main()
    for k, v in f.items():
        print(f"{k:10s} {len(v)}  {v}")
    assert f["exact"] == [1] and f["empty"] == [10] and f["long"] == [11] and f["leaks"] == [0]
    assert (0, 2) in f["near"] or (1, 2) in f["near"]
    assert f["conflicts"] == [(3, 4)]
    print("lesson 5 ok")
