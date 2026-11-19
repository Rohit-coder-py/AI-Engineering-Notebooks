"""
================================================================================
DAY 1 — Variables, Assignment & Reassignment (Deep Dive)
================================================================================

INTERVIEW MINDSET: Don't say "a variable is a box that holds a value."
Say: "In Python, a variable is a NAME bound to an OBJECT. Names have no type;
objects do. Assignment creates (or rebinds) that name->object link."

================================================================================
1. WHAT A VARIABLE REALLY IS
================================================================================
C/Java model:  int age = 25;      // 'age' is a typed memory box holding 25
Python model:  age = 25           # 'age' is a name pointing to int object 25

       name        object (on the heap)
   -------       ------------------
   age  --------> [ 25 ]  <class 'int'>
   name --------> [ "Amit" ] <class 'str'>

Key implications:
  * Variables have NO type; the OBJECT they reference has a type.
  * One object can have many names (aliases).
  * A name can be rebound to an object of an entirely different type.
================================================================================
"""

# Assignment binds a name to an object.
age = 25
name = "Amit"

print(age, name)           # 25 Amit
print(type(age))           # <class 'int'>  -> type of the object, not the name
print(type(name))          # <class 'str'>

# id() shows the object's memory address (identity).
print(id(age))             # some integer, e.g. 140712345678912

# ------------------------------------------------------------------------------
# 2. VARIABLE ASSIGNMENT
# ------------------------------------------------------------------------------
# Syntax: <name> = <expression>
# The RHS expression is evaluated FIRST, then the name is bound to the result.

x = 10
y = x + 5                  # RHS evaluates to 15, then 'y' is bound to 15
print(x, y)                # 10 15

# ------------------------------------------------------------------------------
# 3. VARIABLE REASSIGNMENT
# ------------------------------------------------------------------------------
# Rebinding an existing name to a NEW object. The old object isn't destroyed by
# the statement itself; Python's garbage collector reclaims it when nothing
# references it anymore (reference counting + generational GC).

counter = 1                # counter -> int object 1
counter = 2                # counter -> int object 2
counter = "two"            # counter -> str object "two"   (dynamic typing)
print(counter)             # two

# IMPORTANT interview distinction: REASSIGNMENT vs MUTATION
#   Reassignment  -> name now points to a different object
#   Mutation      -> same object, contents changed in place (mutables only)

a = [1, 2, 3]
a = [4, 5, 6]              # REASSIGNMENT: 'a' points to a NEW list object
print("reassign:", a)      # [4, 5, 6]

b = [1, 2, 3]
b.append(4)                # MUTATION: same list object, contents changed
print("mutate:  ", b)      # [1, 2, 3, 4]

# Immutable objects (int, str, tuple) cannot be mutated — any "change"
# creates a new object and rebinds the name.
s = "hello"
# s[0] = "H"              # TypeError: 'str' object does not support item assignment
s = "Hello"                # new string object, 's' rebound
print(s)                   # Hello

# ------------------------------------------------------------------------------
# 4. NAMING CONVENTIONS (PEP 8)
# ------------------------------------------------------------------------------
# Valid names: letters, digits, underscore; cannot start with a digit.
# Case-sensitive: Age != age != AGE.

# Recommended: snake_case for variables and functions.
user_name = "rohit"
total_amount = 1000
is_active = True

# Module-level constants (convention only, not enforced): UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
PI = 3.14159

# Avoid/Reserved-by-convention:
#   _temp          -> "internal/private" hint
#   __name         -> name mangling inside classes (avoid for plain variables)
#   single letter  -> OK only in tiny loops/math (i, x, dx)
#   keywords       -> cannot be used as names (see keyword module below)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5. RESERVED KEYWORDS (cannot be used as variable names)
# ------------------------------------------------------------------------------
import keyword

print("Keyword count:", len(keyword.kwlist))      # 35 in modern Python 3
print("Examples:    ", keyword.kwlist[:10])       # ['False','None','True','and',...]

# class = 10   -> SyntaxError (uncomment to see)

# ------------------------------------------------------------------------------
# INTERVIEW QUESTIONS (answers as comments)
# ------------------------------------------------------------------------------
# Q1. Are Python variables statically or dynamically typed?
# A: Dynamically typed — a name's type is determined at runtime by the object
#    it currently references. A name can be rebound to objects of different types.
#
# Q2. Is Python strongly or weakly typed?
# A: Strongly typed — Python does NOT implicitly coerce unrelated types.
#    "5" + 2 raises TypeError (unlike JS, which would coerce).
#
# Q3. Can a variable name start with a digit?
# A: No. 1abc = 10 is a SyntaxError.
#
# Q4. What is the difference between assignment and mutation?
# A: Assignment rebinds a name to an object. Mutation changes an object's
#    contents in place. Only mutable objects (list, dict, set, bytearray) can
#    be mutated; immutable ones (int, str, tuple, frozenset, bytes) cannot.

if __name__ == "__main__":
    print("Module run directly — see printed output above.")
