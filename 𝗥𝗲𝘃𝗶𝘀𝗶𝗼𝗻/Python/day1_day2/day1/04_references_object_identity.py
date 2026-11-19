"""
================================================================================
DAY 1 — References and Object Identity (the most-asked internship topic)
================================================================================

INTERVIEW MINDSET: You must be able to explain id(), is vs ==, interning,
mutability, and why "Python variables are references, not boxes."
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. EVERYTHING IS AN OBJECT
# ------------------------------------------------------------------------------
# Every value in Python is an object with three things:
#   (1) identity   — memory address, via id()
#   (2) type       — via type()
#   (3) value      — the actual data
#   (4) refcount   — how many names refer to it (CPython detail)

obj = 42
print("id:", id(obj))      # identity (memory address in CPython)
print("type:", type(obj))  # <class 'int'>
print("value:", obj)       # 42

# ------------------------------------------------------------------------------
# 2. id() — OBJECT IDENTITY
# ------------------------------------------------------------------------------
# id(x) returns a unique integer for the object during its lifetime.
# Two variables with the same id point to the SAME object.

x = 1000
y = 1000
print(id(x) == id(y))      # False — separate int objects (no interning for large ints)

x = 1000
y = x
print(id(x) == id(y))      # True — same object

# ------------------------------------------------------------------------------
# 3. is vs ==   (CRITICAL INTERVIEW QUESTION)
# ------------------------------------------------------------------------------
#   ==  : EQUALITY — are the VALUES the same?  (calls __eq__)
#   is  : IDENTITY — are they the SAME OBJECT? (compares id())

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)              # True  — same contents
print(a is b)              # False — different objects in memory
print(a is c)              # True  — same object

# Never use 'is' to compare values (ints, strings) unless you specifically
# need identity (e.g., checking for None).
print([] is [])            # False
print("" is "")            # may be True (string interning) - DON'T RELY ON IT

# Correct way to check for None:
x = None
print(x is None)           # True   <- idiomatic
# print(x == None)         # works but unidiomatic

# ------------------------------------------------------------------------------
# 4. SMALL INTEGER CACHING & STRING INTERNING
# ------------------------------------------------------------------------------
# CPython caches small integers -5 to 256. Reusing them yields the same object.

x = 256
y = 256
print(x is y)              # True  (cached)

x = 257
y = 257
print(x is y)              # False (usually — may vary at REPL vs script)

# String interning: small / compile-time-known strings may be interned.
s1 = "hello"
s2 = "hello"
print(s1 is s2)            # often True (interned)

s3 = "hello world!"        # longer / computed -> may not be interned
s4 = "hello world!"
print(s3 is s4)            # often False

# Force interning:
import sys
s5 = sys.intern("intern_me")
s6 = sys.intern("intern_me")
print(s5 is s6)            # True

# ------------------------------------------------------------------------------
# 5. MUTABLE vs IMMUTABLE OBJECTS
# ------------------------------------------------------------------------------
# Immutable: int, float, str, bool, tuple, frozenset, bytes, None
#   Cannot be changed in place; "modification" creates a NEW object.
# Mutable:   list, dict, set, bytearray, custom objects
#   Can be changed in place; all names pointing to it see the change.

imm = (1, 2, 3)
# imm[0] = 9               # TypeError: 'tuple' object does not support item assignment

mut = [1, 2, 3]
mut[0] = 9                 # OK — mutated in place
print(mut)                 # [9, 2, 3]

# ------------------------------------------------------------------------------
# 6. REFERENCES & ALIASING — CLASSIC GOTCHA
# ------------------------------------------------------------------------------
original = [1, 2, 3]
alias = original           # alias points to the SAME list
alias.append(4)
print(original)            # [1, 2, 3, 4]  <- original changed too!

# To copy a list (shallow copy):
copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]
copy4 = original.__copy__()   # rarely used directly

copy1.append(99)
print(original)            # [1, 2, 3, 4]  (unchanged by copy1's append)

# NOTE: .copy() / slicing is SHALLOW — nested mutable objects are still shared.
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
shallow[0].append(99)
print(nested)              # [[1, 2, 99], [3, 4]]  <- inner list shared!

# For a deep copy, use the copy module:
import copy
deep = copy.deepcopy(nested)
deep[0].append(77)
print(nested)              # [[1, 2, 99], [3, 4]]  (unchanged now)

# ------------------------------------------------------------------------------
# 7. REFERENCE COUNTING & GARBAGE COLLECTION (brief)
# ------------------------------------------------------------------------------
# CPython keeps a reference count per object. When it hits 0, memory is freed.
# Cycles (a -> b -> a) are handled by the cyclic garbage collector.
# You rarely manage this manually, but knowing it explains why objects "disappear."

import sys
a = [1, 2, 3]
print(sys.getrefcount(a))   # includes the temporary argument to getrefcount

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Difference between '==' and 'is'?
# A: '==' compares VALUES (equality, __eq__). 'is' compares IDENTITY (same object,
#    same id()). Use 'is' only for singletons like None, True, False.
#
# Q: Why is [] is [] False?
# A: Each list literal creates a new list object in memory; they have different ids.
#
# Q: What happens when you do b = a for a list, then mutate b?
# A: Both names refer to the same object, so the mutation is visible via a too.
#    Use .copy() / list(a) / a[:] for an independent shallow copy.

if __name__ == "__main__":
    print("Run directly to see identity and interning behavior.")
