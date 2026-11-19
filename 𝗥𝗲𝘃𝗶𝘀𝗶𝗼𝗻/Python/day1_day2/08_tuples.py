"""
DAY 2 | 08 - TUPLES
===================
Immutability, packing/unpacking, single-element gotcha, hashability,
namedtuple, when to use tuple vs list.

Run: python 08_tuples.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. THEORY")
# ----------------------------------------------------------------------
# tuple = ordered, IMMUTABLE sequence. Allows duplicates and mixed types.
# - The tuple's structure can't change (no add/remove/replace items)
# - But if it holds a mutable object, THAT object can still change.
# - Hashable if ALL its items are hashable -> usable as dict key / set member.
# - Slightly faster and smaller than list; signals "fixed record".
t = (1, 2, 3)
print(t, type(t), len(t), t[0], t[-1], t[1:], t * 2, t + (4,))
print(2 in t, t.count(2), t.index(3))

# ----------------------------------------------------------------------
section("2. CREATING TUPLES - the comma makes the tuple")
# ----------------------------------------------------------------------
a = (5)        # int!
b = (5,)       # tuple with one element
c = 5,         # also a tuple
d = ()         # empty tuple
e = 1, 2, 3    # parentheses optional
print(type(a), type(b), type(c), type(d), type(e))
print(tuple("abc"), tuple([1, 2]), tuple(range(3)))

# ----------------------------------------------------------------------
section("3. IMMUTABILITY")
# ----------------------------------------------------------------------
t = (1, 2, 3)
try:
    t[0] = 9
except TypeError as err:
    print("TypeError:", err)

# "Changing" a tuple = creating a new one
t = t + (4,)
print(t)
lst = list(t); lst[0] = 100; t = tuple(lst)
print(t)

# Mutable inside immutable
info = ("Harsh", [90, 80])
info[1].append(70)           # allowed
print(info)
# info[1] += [60] -> mutates the list AND raises TypeError (famous trap)
try:
    info[1] += [60]
except TypeError as err:
    print("TypeError but list still changed ->", info)

# ----------------------------------------------------------------------
section("4. PACKING & UNPACKING")
# ----------------------------------------------------------------------
point = (3, 4)          # packing
x, y = point            # unpacking
print(x, y)
first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)     # middle is a LIST
x, y = y, x                    # swap: RHS tuple built first, then unpacked
print(x, y)
for i, (name, mark) in enumerate([("A", 90), ("B", 80)]):
    print(i, name, mark)
def min_max(nums):
    return min(nums), max(nums)        # returning multiple values = returning a tuple
lo, hi = min_max([4, 1, 9])
print(lo, hi, min_max([4, 1, 9]))

# ----------------------------------------------------------------------
section("5. HASHABLE -> dict keys / set members")
# ----------------------------------------------------------------------
grid = {(0, 0): "start", (1, 2): "treasure"}
print(grid[(1, 2)])
print({(1, 2), (1, 2), (2, 1)})
try:
    {[1, 2]: "x"}
except TypeError as err:
    print("list as key ->", err)
try:
    hash((1, [2]))
except TypeError as err:
    print("tuple containing list unhashable ->", err)

# ----------------------------------------------------------------------
section("6. COMPARISON & SORTING")
# ----------------------------------------------------------------------
print((1, 2, 3) < (1, 2, 4), (1, 9) < (2, 0))     # lexicographic
people = [("Ravi", 30), ("Amit", 25), ("Neha", 30)]
print(sorted(people, key=lambda p: (-p[1], p[0])))  # age desc, then name asc

# ----------------------------------------------------------------------
section("7. namedtuple - readable immutable records")
# ----------------------------------------------------------------------
from collections import namedtuple
Student = namedtuple("Student", ["name", "roll", "marks"])
s = Student("Harsh", 7, 91.5)
print(s, s.name, s[1], s._asdict())
print(s._replace(marks=95))        # new tuple, original unchanged

# ----------------------------------------------------------------------
section("8. TUPLE vs LIST")
# ----------------------------------------------------------------------
import sys
print("size list :", sys.getsizeof([1, 2, 3]))
print("size tuple:", sys.getsizeof((1, 2, 3)))
# Use TUPLE for: fixed records (x, y), dict keys, function returns, data that
#                must not change, heterogeneous items.
# Use LIST  for: homogeneous collection that grows/shrinks/gets sorted.

# ----------------------------------------------------------------------
section("9. PREDICT THE OUTPUT")
# ----------------------------------------------------------------------
print(type((1)), type((1,)), type(()))              # ?
t = (1, 2, [3, 4])
t[2][0] = 99
print(t)                                            # ?
print((1, 2) + (3,), (1, 2) * 2)                    # ?
a, b, *c = (1, 2)
print(a, b, c)                                      # ?
print(len((1, (2, 3), 4)))                          # ?
