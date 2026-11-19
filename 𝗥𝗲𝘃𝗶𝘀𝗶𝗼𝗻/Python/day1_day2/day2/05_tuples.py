"""
================================================================================
DAY 2 — Tuples (immutable ordered sequences)
================================================================================

INTERVIEW MINDSET: Tuples are immutable, hashable (if contents are hashable),
can be dict keys, and support packing/unpacking. Immutability != the object
can't change if it holds a mutable element (tuple of lists).
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. CREATION
# ------------------------------------------------------------------------------
point = (10, 20)              # with parentheses
point = 10, 20                # without (tuple packing) — identical

singleton = (42,)             # COMMA REQUIRED — otherwise it's just (42) = int 42
not_a_tuple = (42)            # this is an int!
empty = ()                    # empty tuple

print(type(singleton))        # <class 'tuple'>
print(type(not_a_tuple))      # <class 'int'>

# ------------------------------------------------------------------------------
# 2. IMMUTABILITY
# ------------------------------------------------------------------------------
point = (10, 20)
# point[0] = 99               # TypeError: 'tuple' object does not support item assignment
# point.append(30)            # AttributeError: 'tuple' object has no attribute 'append'

# You can only create a NEW tuple:
point = (99, 20)              # rebind name to a new tuple object

# GOTCHA: immutability is shallow — mutable elements inside can still change
t = (1, 2, [3, 4])
t[2].append(5)                # OK! the LIST inside is mutated
print(t)                      # (1, 2, [3, 4, 5])  — tuple object unchanged, contents changed

# ------------------------------------------------------------------------------
# 3. INDEXING & SLICING (same as lists)
# ------------------------------------------------------------------------------
t = (10, 20, 30, 40, 50)
print(t[0])           # 10
print(t[-1])          # 50
print(t[1:4])         # (20, 30, 40)
print(t[::2])         # (10, 30, 50)

# ------------------------------------------------------------------------------
# 4. TUPLE OPERATIONS
# ------------------------------------------------------------------------------
t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)        # (1, 2, 3, 4)   concatenation -> new tuple
print(t1 * 3)         # (1, 2, 1, 2, 1, 2) repetition -> new tuple
print(len(t1))        # 2
print(2 in t1)        # True
print(t1.index(2))    # 1
print(t1.count(1))    # 1

# ------------------------------------------------------------------------------
# 5. PACKING & UNPACKING
# ------------------------------------------------------------------------------
# Packing:
person = ("Rohit", 25, "Pune")   # tuple packing

# Unpacking:
name, age, city = person
print(name, age, city)           # Rohit 25 Pune

# Swap via tuple unpacking (from Day 1):
a, b = 1, 2
a, b = b, a

# Nested unpacking:
data = ("Alice", ("Engineering", "Python"))
name, (dept, lang) = data
print(name, dept, lang)          # Alice Engineering Python

# ------------------------------------------------------------------------------
# 6. NAMEDTUPLE (lightweight immutable record)
# ------------------------------------------------------------------------------
from collections import namedtuple

# Creates a tuple subclass with named fields — great for returning records.
Employee = namedtuple("Employee", ["name", "age", "city"])
e = Employee("Rohit", 25, "Pune")

print(e.name, e.age, e.city)     # Rohit 25 Pune   (attribute access)
print(e[0], e[1], e[2])          # Rohit 25 Pune   (index access still works)
print(e._asdict())               # {'name': 'Rohit', 'age': 25, 'city': 'Pune'}

# ------------------------------------------------------------------------------
# 7. WHEN TUPLE vs LIST?
# ------------------------------------------------------------------------------
# Use tuple when:
#   - data should not change (semantic immutability)
#   - you need a dict key / set member (tuples of hashables are hashable)
#   - returning multiple values from a function
#   - performance/memory matters slightly (tuples are lighter than lists)
# Use list when you need to add/remove/reorder items.

# Tuple as dict key (hashable):
locations = {(40.7128, -74.0060): "New York", (19.0760, 72.8777): "Mumbai"}
print(locations[(19.0760, 72.8777)])   # Mumbai

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Are tuples fully immutable?
# A: The tuple object itself is immutable (can't add/remove/replace items),
#    but if it contains a mutable object (e.g., a list), that inner object
#    can still be mutated.
#
# Q: Can a tuple be a dict key?
# A: Yes, if all its elements are hashable. ((1,2), "key") works;
#    ([1,2], "key") raises TypeError: unhashable type: 'list'.
#
# Q: (42) vs (42,)?
# A: (42) is just the int 42 (parentheses don't make a tuple). (42,) is a
#    one-element tuple — the comma is what matters.

if __name__ == "__main__":
    print("Run directly to see tuple examples.")
