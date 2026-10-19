"""Swipe and match: store each swipe, and on a right swipe look up the reverse swipe with one key lookup.
Run: python3 match.py"""


class Swipes:
    def __init__(self):
        self.right = set()            # (swiper, target) pairs
        self.matches = set()

    def swipe(self, a, b, direction):
        if direction != "right":
            return False
        self.right.add((a, b))
        if (b, a) in self.right:                          # one key lookup for the reverse swipe
            self.matches.add(frozenset((a, b)))           # a set, so the match is created once
            return True
        return False


if __name__ == "__main__":
    s = Swipes()
    r1 = s.swipe("ana", "ben", "right")
    r2 = s.swipe("ben", "ana", "right")
    r3 = s.swipe("ben", "ana", "right")                   # a repeated swipe creates no second match
    r4 = s.swipe("cy", "ana", "left")
    print(f"ana right on ben: {r1}; ben right on ana: {r2} (match); a repeated swipe reports {r3} again; matches stored: {len(s.matches)}")
    assert (r1, r2, r4) == (False, True, False) and len(s.matches) == 1
    print("match ok")
