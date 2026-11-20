"""
================================================================================
DAY 2 — Dictionaries (mutable key-value mappings, hash tables)
================================================================================

INTERVIEW MINDSET: Dicts are hash tables — O(1) average lookup/insert/delete.
Keys must be hashable; values can be anything. Python 3.7+ preserves insertion
order. Know .get() vs [], .setdefault(), views, and dict comprehensions.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. CREATION
# ------------------------------------------------------------------------------
user = {"name": "Rohit", "age": 25, "city": "Pune"}   # dict literal
empty = {}
user2 = dict(name="Amit", age=30)                     # from keyword args

# ------------------------------------------------------------------------------
# 2. ACCESSING VALUES
# ------------------------------------------------------------------------------
print(user["name"])       # Rohit
# print(user["country"])   # KeyError — use .get() to avoid

print(user.get("country"))         # None
print(user.get("country", "India"))# India  (default if missing)

# ------------------------------------------------------------------------------
# 3. ADD / UPDATE / DELETE
# ------------------------------------------------------------------------------
user["country"] = "India"        # add new key
user["age"] = 26                 # update existing

del user["city"]                 # delete by key
country = user.pop("country")    # remove & return value (KeyError if missing)
print("popped:", country)        # India

user.clear()                     # empty the dict
print(user)                      # {}

# ------------------------------------------------------------------------------
# 4. COMMON METHODS
# ------------------------------------------------------------------------------
d = {"a": 1, "b": 2, "c": 3}

print(d.keys())       # dict_keys(['a', 'b', 'c'])
print(d.values())     # dict_values([1, 2, 3])
print(d.items())      # dict_items([('a', 1), ('b', 2), ('c', 3)])

# keys() / values() / items() return VIEWS — they reflect live changes:
view = d.keys()
d["d"] = 4
print(view)           # dict_keys(['a', 'b', 'c', 'd']) — view updated

# setdefault: get value, or set default if missing (useful for grouping)
counts = {}
for letter in "banana":
    counts.setdefault(letter, 0)
    counts[letter] += 1
print(counts)         # {'b': 1, 'a': 3, 'n': 2}

# Alternative: collections.defaultdict
from collections import defaultdict
counts2 = defaultdict(int)
for letter in "banana":
    counts2[letter] += 1
print(dict(counts2))  # {'b': 1, 'a': 3, 'n': 2}

# ------------------------------------------------------------------------------
# 5. DICT COMPREHENSION
# ------------------------------------------------------------------------------
squares = {x: x**2 for x in range(1, 6)}
print(squares)        # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From two lists (zip):
keys = ["name", "age", "city"]
values = ["Rohit", 25, "Pune"]
merged = {k: v for k, v in zip(keys, values)}
print(merged)         # {'name': 'Rohit', 'age': 25, 'city': 'Pune'}

# ------------------------------------------------------------------------------
# 6. KEY REQUIREMENTS — HASHABLE KEYS
# ------------------------------------------------------------------------------
valid = {(1, 2): "point"}                    # tuple of ints — hashable -> OK
# invalid = {[1, 2]: "bad"}                   # TypeError: unhashable type: 'list'

# Values can be ANY type (mutable or not):
mixed = {"list": [1, 2], "dict": {"a": 1}}   # perfectly fine

# ------------------------------------------------------------------------------
# 7. NESTED DICTIONARIES & SAFE ACCESS
# ------------------------------------------------------------------------------
profile = {
    "name": "Rohit",
    "address": {"city": "Pune", "pincode": 411001},
    "skills": ["Python", "SQL"],
}

# Chained access can raise KeyError — use .get() at each level:
city = profile.get("address", {}).get("city")
print(city)        # Pune

# ------------------------------------------------------------------------------
# 8. ORDER (Python 3.7+)
# ------------------------------------------------------------------------------
ordered = {"first": 1, "second": 2, "third": 3}
print(list(ordered.keys()))   # ['first', 'second', 'third'] — insertion order preserved
# Note: dict is ordered by insertion, NOT sorted. For sorted traversal use sorted(d).

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Time complexity of dict operations?
# A: Average O(1) for get/set/delete (hash table). Worst case O(n) on hash
#    collisions. keys()/values()/items() are O(1) views.
#
# Q: Can a list be a dict key?
# A: No — unhashable. Only hashable keys (int, str, tuple-of-hashables,
#    frozenset). Values have no such restriction.
#
# Q: d["key"] vs d.get("key")?
# A: d["key"] raises KeyError if missing. d.get("key") returns None (or a
#    default). Use .get() when the key might be absent.
#
# Q: Are dicts ordered?
# A: Yes, insertion order is guaranteed since Python 3.7 (language spec since 3.8).
#    They are not sorted.

if __name__ == "__main__":
    print("Run directly to see dictionary examples.")
