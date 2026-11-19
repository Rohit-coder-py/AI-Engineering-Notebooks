"""
================================================================================
DAY 2 — Sets & Frozensets (unordered collections of unique items)
================================================================================

INTERVIEW MINDSET: Sets are hash tables — O(1) membership, deduplication,
mathematical set operations (union/intersection/difference/symmetric diff).
Items must be hashable. No indexing.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. CREATION
# ------------------------------------------------------------------------------
fruits = {"apple", "banana", "cherry"}      # set literal
empty_set = set()                           # {} is an EMPTY DICT, not set!

nums = {1, 2, 2, 3, 3, 3}                   # duplicates removed automatically
print(nums)                                 # {1, 2, 3}  (order arbitrary)

# From any iterable:
s = set([1, 2, 2, 3])                       # {1, 2, 3}
s = set("hello")                            # {'h', 'e', 'l', 'o'} — chars

# ------------------------------------------------------------------------------
# 2. BASIC OPERATIONS
# ------------------------------------------------------------------------------
s = {1, 2, 3}

s.add(4)                                    # add single element
print(s)                                    # {1, 2, 3, 4}

s.add(4)                                    # adding duplicate — no-op, no error
print(s)                                    # {1, 2, 3, 4}

s.remove(3)                                 # removes 3; KeyError if missing
print(s)                                    # {1, 2, 4}

s.discard(10)                               # removes if present; NO error if missing
print(s)                                    # {1, 2, 4}

popped = s.pop()                            # removes & returns ARBITRARY element
print("popped:", popped)                    # order not guaranteed

s.clear()
print(s)                                    # set()

# ------------------------------------------------------------------------------
# 3. MEMBERSHIP — O(1) (set's superpower)
# ------------------------------------------------------------------------------
vowels = {"a", "e", "i", "o", "u"}
print("a" in vowels)           # True   (fast hash-table lookup)
print("z" in vowels)           # False

# ------------------------------------------------------------------------------
# 4. MATHEMATICAL SET OPERATIONS
# ------------------------------------------------------------------------------
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)                   # union           -> {1, 2, 3, 4, 5, 6}
print(a & b)                   # intersection    -> {3, 4}
print(a - b)                   # difference      -> {1, 2}
print(b - a)                   # difference      -> {5, 6}
print(a ^ b)                   # symmetric diff  -> {1, 2, 5, 6}

# In-place versions:
a |= b                         # a = a | b
print(a)

# Subset / superset / disjoint:
print({1, 2} <= {1, 2, 3})     # True   (subset)
print({1, 2, 3} >= {1, 2})     # True   (superset)
print({1, 2}.isdisjoint({3, 4}))   # True   (no common elements)

# ------------------------------------------------------------------------------
# 5. FROZENSET (immutable set, hashable)
# ------------------------------------------------------------------------------
fs = frozenset([1, 2, 3])
# fs.add(4)                  # AttributeError — immutable

# Frozensets ARE hashable -> can be set elements or dict keys:
nested = {frozenset([1, 2]), frozenset([3, 4])}
print(nested)                  # {frozenset({1, 2}), frozenset({3, 4})}

key_map = {frozenset(["a", "b"]): "pair"}
print(key_map[frozenset(["a", "b"])])   # pair

# ------------------------------------------------------------------------------
# 6. PRACTICAL PATTERN — DEDUPLICATION WHILE PRESERVING ORDER
# ------------------------------------------------------------------------------
items = ["apple", "banana", "apple", "cherry", "banana"]

# Set loses order:
print(set(items))                       # {'banana', 'apple', 'cherry'} (order arbitrary)

# Preserve order (dict.fromkeys — keys are unique, dict preserves insertion order):
unique = list(dict.fromkeys(items))
print(unique)                           # ['apple', 'banana', 'cherry']

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Time complexity of set operations?
# A: add / remove / discard / in — average O(1) (hash table). Union/intersection
#    — O(len of operands).
#
# Q: Can you index a set? s[0]?
# A: No. Sets are unordered and unindexed. Convert to list first if needed.
#
# Q: {} vs set() for empty set?
# A: {} creates an empty DICT. set() creates an empty SET.
#
# Q: What must set items be?
# A: Hashable (immutable): int, str, tuple-of-hashables, frozenset.
#    Not hashable: list, dict, set -> TypeError.

if __name__ == "__main__":
    print("Run directly to see set examples.")
