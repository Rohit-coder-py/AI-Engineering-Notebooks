"""
DAY 1 | 01 - VARIABLES
=======================
Covers: assignment, reassignment, how variables work internally, naming
conventions, dynamic typing, multiple assignment, references & object identity.

Run:  python 01_variables.py
Tip : Read the comments first, PREDICT the output, then run and compare.
"""
import sys


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. WHAT IS A VARIABLE? (Names bound to objects)")
# ----------------------------------------------------------------------
# THEORY
# In Python a variable is NOT a box that stores a value (C/Java mental model).
# A variable is a NAME (label) that is BOUND to an OBJECT living in memory.
#     x = 10
#   1) Python creates an int object with value 10 (or reuses a cached one)
#   2) The name 'x' is bound (points) to that object.
# Every object has: identity -> id(), type -> type(), value.
# '=' is the "binding" operator, not "copy value into box".

x = 10
print("x =", x, "| type:", type(x), "| id:", id(x))

# ----------------------------------------------------------------------
section("2. ASSIGNMENT & REASSIGNMENT")
# ----------------------------------------------------------------------
# Reassignment does NOT change the old object. It re-binds the name to a
# NEW object. The old object is garbage collected if nothing points to it.
a = 5
print("before:", a, id(a))
a = a + 1  # new int object (6) created, 'a' now points to it
print("after :", a, id(a))

a = "now I am a string"  # same name, completely different type -> fine
print(a, type(a))

# Augmented assignment
n = 10
n += 5   # n = n + 5
n *= 2   # n = n * 2
n -= 1
n //= 3
print("n after augmented ops:", n)

# ----------------------------------------------------------------------
section("3. HOW VARIABLES WORK INTERNALLY")
# ----------------------------------------------------------------------
# THEORY (CPython)
# - Names live in a namespace, which is basically a dict:  {'x': <object>}
# - Each object has a reference count (how many names/containers point to it)
# - When refcount hits 0, memory is freed (plus a cyclic garbage collector
#   for reference cycles).
print("Module namespace has 'x'? ->", "x" in globals())
print("globals()['x'] ->", globals()["x"])

lst = [1, 2, 3]
# getrefcount shows +1 because passing it as an argument creates a temp ref
print("refcount of lst:", sys.getrefcount(lst))
alias = lst
print("refcount after alias:", sys.getrefcount(lst))
del alias  # 'del' removes the NAME, not the object
print("refcount after del alias:", sys.getrefcount(lst))

# Small integer caching (CPython implementation detail: -5 to 256)
p = int("256")
q = int("256")
print("256 is 256 ->", p is q)   # True  (cached)
p = int("257")
q = int("257")
print("257 is 257 ->", p is q)   # False (two separate objects)
print("257 == 257 ->", p == q)   # True  (same value)
# INTERVIEW: never rely on 'is' for numbers/strings. Use == for values.

# String interning (also an implementation detail)
s1 = "hello"
s2 = "hello"
print("'hello' is 'hello' ->", s1 is s2)  # usually True (interned identifier-like strings)
s3 = "hello world!"
s4 = "".join(["hello", " world!"])
print("runtime built string is same object? ->", s3 is s4)  # usually False

# ----------------------------------------------------------------------
section("4. NAMING CONVENTIONS (PEP 8)")
# ----------------------------------------------------------------------
# RULES (hard, enforced by Python)
#   - start with letter or underscore, never a digit
#   - only letters, digits, underscore
#   - case-sensitive: age, Age, AGE are 3 different names
#   - cannot be a keyword (if, for, class, None, True ...)
# CONVENTIONS (soft, PEP 8)
#   snake_case      -> variables, functions    (student_name)
#   UPPER_SNAKE     -> constants               (MAX_RETRIES = 3)
#   PascalCase      -> classes                 (BankAccount)
#   _single_lead    -> "internal use" hint     (_cache)
#   __double_lead   -> name mangling in classes
#   __dunder__      -> special/magic names     (__init__) - don't invent your own
#   single_trail_   -> avoid clash with keyword (class_)
import keyword

print("Keywords count:", len(keyword.kwlist))
print(keyword.kwlist)

student_name = "Harsh"      # good
MAX_ATTEMPTS = 3            # constant by convention (Python won't stop you from changing it)
_internal_counter = 0       # internal hint
print(student_name, MAX_ATTEMPTS, _internal_counter)

# Bad examples (commented because they'd be errors or poor style):
#   2name = "x"     -> SyntaxError (starts with digit)
#   my-var = 1      -> SyntaxError (hyphen is minus)
#   class = 5       -> SyntaxError (keyword)
#   l, O, I as names -> legal but confusing (look like 1 and 0)

# ----------------------------------------------------------------------
section("5. DYNAMIC TYPING")
# ----------------------------------------------------------------------
# THEORY
# Types belong to OBJECTS, not to names. A name can point to any type at any time.
# Python is dynamically typed (type checked at runtime) AND strongly typed
# (no silent unsafe coercion: "5" + 5 raises TypeError).
v = 42
print(type(v))
v = 3.14
print(type(v))
v = [1, 2]
print(type(v))

try:
    print("5" + 5)
except TypeError as e:
    print("Strong typing ->", e)

# Optional type hints are documentation/tooling only; NOT enforced at runtime.
count: int = 10
count = "ten"  # no error at runtime!
print("type hints don't enforce:", count)

# ----------------------------------------------------------------------
section("6. MULTIPLE ASSIGNMENT")
# ----------------------------------------------------------------------
# a) Same value to many names (all point to the SAME object)
a = b = c = 0
print(a, b, c, id(a) == id(b) == id(c))

# b) Different values, one line (tuple packing / unpacking)
x, y, z = 1, 2, 3
print(x, y, z)

# c) Swap without temp variable
x, y = y, x
print("swapped:", x, y)

# d) Star unpacking
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)

# e) Unpack nested
(m, n), o = (1, 2), 3
print(m, n, o)

# f) Ignore values with _
_, second, _ = ("a", "b", "c")
print(second)

# GOTCHA with chained assignment + mutable objects
l1 = l2 = []          # SAME list
l1.append(1)
print("l2 also changed:", l2)
l3, l4 = [], []       # two DIFFERENT lists
l3.append(1)
print("l4 unchanged:", l4)

# ----------------------------------------------------------------------
section("7. REFERENCES & OBJECT IDENTITY")
# ----------------------------------------------------------------------
# == compares VALUES (calls __eq__)
# is compares IDENTITY (same object in memory, id(a) == id(b))
a = [1, 2, 3]
b = a            # b is another name for the same list (alias)
c = [1, 2, 3]    # equal value, different object
print("a == c:", a == c, "| a is c:", a is c)
print("a is b:", a is b)

b.append(4)      # mutate through alias
print("a after b.append(4):", a)   # a changed too!

# Immutable vs mutable behaviour on "modification"
t = "abc"
t_id = id(t)
t += "d"        # strings immutable -> NEW object
print("string id changed:", t_id != id(t))

nums = [1]
nums_id = id(nums)
nums += [2]     # list += is in-place for mutable list
print("list id same:", nums_id == id(nums))

# Passing to functions: "pass by object reference" (a.k.a. call by sharing)
def mutate(lst):
    lst.append("changed")      # mutates caller's object

def rebind(lst):
    lst = ["new list"]         # only rebinds local name; caller unaffected

data = [1]
mutate(data)
print("after mutate:", data)
rebind(data)
print("after rebind:", data)

# Correct use of 'is': compare with singletons
val = None
print("val is None:", val is None)

# Copying
orig = [[1, 2], [3, 4]]
shallow = orig.copy()
import copy
deep = copy.deepcopy(orig)
orig[0].append(99)
print("shallow sees change:", shallow)   # inner list shared
print("deep unaffected    :", deep)

# ----------------------------------------------------------------------
print("\nDONE. Now open 11_interview_theory.md and search 'variable' for questions.")
