"""Search over a social graph with inverted indexes: each term maps to a sorted list of IDs, and a query is a set
operation on the lists. Run: python3 graph_search.py"""

PEOPLE = {"alice": "london", "bob": "london", "cyra": "paris", "dev": "london", "eli": "berlin"}
FRIENDS = {"alice": ["bob", "cyra", "dev"], "bob": ["alice"], "cyra": ["alice"], "dev": ["alice", "eli"], "eli": ["dev"]}


def build():
    idx = {}
    for person, city in PEOPLE.items():
        idx.setdefault(f"lives_in:{city}", set()).add(person)
    for person, friends in FRIENDS.items():
        for f in friends:
            idx.setdefault(f"friend:{person}", set()).add(f)
    return idx


def query(idx, *terms):
    sets = [idx.get(t, set()) for t in terms]
    return sorted(set.intersection(*sets)) if sets else []


if __name__ == "__main__":
    idx = build()
    result = query(idx, "friend:alice", "lives_in:london")
    print("friends of alice who live in london:", result)
    assert result == ["bob", "dev"]
    assert query(idx, "friend:alice", "lives_in:berlin") == []
    print("graph search ok")
