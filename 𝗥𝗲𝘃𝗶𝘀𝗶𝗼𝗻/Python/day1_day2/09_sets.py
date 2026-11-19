"""
DAY 2 | 09 - SETS
==================
Creation, uniqueness, set algebra, methods, frozenset, hashing,
performance, common patterns.

Run: python 09_sets.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. THEORY")
# ----------------------------------------------------------------------
# set = UNORDERED collection of UNIQUE, HASHABLE elements. Mutable itself.
# Internally a hash table -> membership test, add, remove are O(1) average.
# No indexing / slicing (no order). Iteration order is arbitrary (don't rely on it).
s = {3, 1, 2, 3, 1}
print(s, len(s))
print(set("hello"), set([1, 2, 2]), set())
empty_dict = {}
empty_set = set()                 # {} is a DICT, not a set!
print(type(empty_dict), type(empty_set))
# Elements must be hashable:
try:
    {[1, 2], 3}
except TypeError as e:
    print("TypeError:", e)
print({(1, 2), "a", 5, 2.5, True})  # note True == 1 hashing

# ----------------------------------------------------------------------
section("2. ADD / REMOVE")
# ----------------------------------------------------------------------
s = {1, 2, 3}
s.add(4)               # no effect if present
s.add(2)
s.update([5, 6], {7})  # add many
print(s)
s.remove(7)            # KeyError if missing
s.discard(100)         # no error if missing
print(s.pop() in {1, 2, 3, 4, 5, 6})  # removes an ARBITRARY element
s.clear()
print(s)
try:
    {1}.remove(5)
except KeyError as e:
    print("KeyError:", e)

# ----------------------------------------------------------------------
section("3. SET ALGEBRA")
# ----------------------------------------------------------------------
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
print("union        :", A | B, A.union(B))
print("intersection :", A & B, A.intersection(B))
print("difference   :", A - B, A.difference(B))     # in A not in B
print("sym. diff    :", A ^ B, A.symmetric_difference(B))
print("subset       :", {1, 2} <= A, {1, 2}.issubset(A))
print("superset     :", A >= {1, 2}, A.issuperset({1}))
print("disjoint     :", A.isdisjoint({9, 10}))
# In-place versions: |=  &=  -=  ^=   (or update, intersection_update, ...)
A |= {10}
print(A)
# Methods accept any iterable, operators need sets:
print({1, 2}.union([3, 4]))
# {1,2} | [3,4] -> TypeError

# ----------------------------------------------------------------------
section("4. COMPREHENSION & frozenset")
# ----------------------------------------------------------------------
print({x % 5 for x in range(20)})
fs = frozenset([1, 2, 3])          # immutable & hashable
print(fs, {fs: "can be a dict key"}, {frozenset({1}), frozenset({1})})
# fs.add(4) -> AttributeError

# ----------------------------------------------------------------------
section("5. WHY SETS? PERFORMANCE")
# ----------------------------------------------------------------------
import time
big_list = list(range(200_000))
big_set = set(big_list)
target = 199_999
t0 = time.perf_counter(); target in big_list; t_list = time.perf_counter() - t0
t0 = time.perf_counter(); target in big_set; t_set = time.perf_counter() - t0
print(f"list lookup: {t_list:.6f}s | set lookup: {t_set:.8f}s")

# ----------------------------------------------------------------------
section("6. COMMON PATTERNS")
# ----------------------------------------------------------------------
# a) Remove duplicates
nums = [3, 1, 3, 2, 1]
print(list(set(nums)))                    # order lost
print(list(dict.fromkeys(nums)))          # order kept

# b) Common / unique elements
a, b = [1, 2, 3, 4], [3, 4, 5]
print("common:", set(a) & set(b), "only in a:", set(a) - set(b))

# c) Check duplicates
print("has duplicates:", len(nums) != len(set(nums)))

# d) First non-repeating / unique characters
text = "programming"
print("unique chars:", len(set(text)), "| sorted:", "".join(sorted(set(text))))

# e) Anagram check using sorted / Counter
from collections import Counter
print(sorted("listen") == sorted("silent"), Counter("listen") == Counter("silent"))

# f) Pangram
import string
print(set(string.ascii_lowercase) <= set("the quick brown fox jumps over the lazy dog"))

# g) Seen-tracking in loops
seen, dup = set(), set()
for n in [1, 2, 3, 2, 4, 1]:
    if n in seen:
        dup.add(n)
    seen.add(n)
print("duplicates:", dup)

# ----------------------------------------------------------------------
section("7. GOTCHAS")
# ----------------------------------------------------------------------
print(1 == True, {1, True, 1.0})          # all equal -> one element
print(len({0, False, 0.0}))               # 1
# Sets are unordered: never index them. sorted(s) gives a list.
# Mutating a set while iterating raises RuntimeError.
# set of lists impossible -> convert inner lists to tuples.

# ----------------------------------------------------------------------
section("8. PREDICT THE OUTPUT")
# ----------------------------------------------------------------------
print(len({1, 2, 2, 3, "a", "a"}))        # ?
print({1, 2} == {2, 1})                   # ?
print({1, 2, 3} - {2} | {9})              # ?  (precedence: - before |)
print(type({}), type({1}), type({1: 1}))  # ?
print(sorted({"b", "a", "c"}))            # ?
