"""
================================================================================
DAY 1 — Python Data Types (with internship-level depth)
================================================================================

INTERVIEW MINDSET: Know the type hierarchy, mutability of each type, bool<int>
relationship, arbitrary-precision ints, and why dict keys must be hashable.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. PYTHON'S TYPE HIERARCHY (everything inherits from object)
# ------------------------------------------------------------------------------
print(type(10))            # <class 'int'>
print(type(10.5))          # <class 'float'>
print(type("hi"))          # <class 'str'>
print(type(True))          # <class 'bool'>
print(type(None))          # <class 'NoneType'>

# All objects ultimately derive from object:
print(int.__bases__)       # (<class 'object'>,)

# ------------------------------------------------------------------------------
# 2. NUMERIC TYPES
# ------------------------------------------------------------------------------
# int: arbitrary precision in Python 3 (no overflow!). Limited only by memory.
big = 2 ** 1000
print(big)                 # huge number — no OverflowError

# float: IEEE 754 double precision (64-bit)
pi = 3.14159
sci = 1.5e-3

# complex
z = 3 + 4j
print(z.real, z.imag)      # 3.0 4.0

# bool: subclass of int; True == 1, False == 0
print(True == 1)           # True
print(False == 0)          # True
print(sum([True, True, False]))   # 2

# ------------------------------------------------------------------------------
# 3. TEXT SEQUENCE TYPE — str
# ------------------------------------------------------------------------------
# Strings are immutable Unicode sequences.
greeting = "Hello, World"
print(len(greeting))       # 13
print(greeting[0])         # H
print(greeting[-1])        # d
print(greeting[0:5])       # Hello  (slicing — start inclusive, end exclusive)

# String methods return NEW strings (immutability):
name = " rohit "
print(name.strip())        # "rohit"
print(name)                # " rohit "  (unchanged)

# f-strings (preferred modern formatting):
age = 25
print(f"{name.strip()} is {age} years old")

# ------------------------------------------------------------------------------
# 4. NONE TYPE
# ------------------------------------------------------------------------------
nothing = None
print(nothing is None)     # True
# None is a singleton — there is exactly one None object in a program.

# ------------------------------------------------------------------------------
# 5. OTHER BUILT-IN TYPES (preview — details in Day 2 files)
# ------------------------------------------------------------------------------
# list   [1, 2, 3]        mutable, ordered, allows duplicates
# tuple  (1, 2, 3)        immutable, ordered
# set    {1, 2, 3}        mutable, unordered, no duplicates, hashable items
# frozenset                immutable set
# dict   {"a": 1}         mutable mapping, hashable keys
# bytes  b"abc"           immutable byte sequence
# bytearray                  mutable byte sequence

example_list = [1, 2, 3]
example_tuple = (1, 2, 3)
example_set = {1, 2, 3}
example_dict = {"name": "rohit", "age": 25}

# ------------------------------------------------------------------------------
# 6. WHY DICT KEYS / SET ITEMS MUST BE HASHABLE
# ------------------------------------------------------------------------------
# Hashable = has __hash__() that never changes + __eq__(). Immutable built-ins
# (int, str, tuple-of-immutables) are hashable. Mutable ones (list, dict, set)
# are NOT, because their hash would change as contents change.

valid_dict = {(1, 2): "point"}     # tuple of immutables -> hashable -> OK
# invalid_dict = {[1, 2]: "bad"}   # TypeError: unhashable type: 'list'

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Does Python int overflow?
# A: No. Python 3 ints are arbitrary precision, limited only by available memory.
#
# Q: Is bool a separate type from int?
# A: bool is a subclass of int. True == 1 and False == 0. That's why sum()
#    works on a list of booleans.
#
# Q: Are strings mutable?
# A: No. str is immutable. Methods like .upper(), .strip(), .replace() return
#    new strings; they never modify the original.
#
# Q: What makes an object hashable, and why does it matter for dicts/sets?
# A: An object is hashable if its hash value never changes during its lifetime
#    (immutable) and it supports equality comparison. Dict keys and set members
#    must be hashable so they can be looked up in O(1) via hash tables.

if __name__ == "__main__":
    print("Run directly to see data type examples.")
