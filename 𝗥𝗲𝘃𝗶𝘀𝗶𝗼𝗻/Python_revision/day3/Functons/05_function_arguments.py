"""
================================================================================
DAY 3 - B2. FUNCTION ARGUMENTS
================================================================================

INTERVIEW MINDSET
-----------------
Argument handling is one of the highest-yield interview topics because it
reveals whether you understand Python's calling model.

Say: "Python binds arguments to parameters at CALL time. It supports
      positional, keyword, default, positional-only, keyword-only,
      *args and **kwargs, plus unpacking at the call site. Defaults are
      evaluated ONCE at definition time - which is why mutable defaults
      are dangerous."

Call model in one line:
  CALL SITE  ->  argument matching  ->  parameter names  ->  local scope
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. POSITIONAL ARGUMENTS
# ------------------------------------------------------------------------------
# Values are matched to parameters by ORDER. The first argument goes to the
# first parameter, and so on.

def describe(name, age, city):
    return f"{name} is {age} and lives in {city}"

print(describe("Rohit", 25, "Pune"))     # Rohit is 25 and lives in Pune

# Too few / too many positional arguments -> TypeError.
try:
    describe("Rohit", 25)
except TypeError as exc:
    print("TypeError:", exc)     # missing 1 required positional argument: 'city'

try:
    describe("Rohit", 25, "Pune", "extra")
except TypeError as exc:
    print("TypeError:", exc)     # takes 3 positional arguments but 4 were given


# ------------------------------------------------------------------------------
# 2. KEYWORD ARGUMENTS
# ------------------------------------------------------------------------------
# Values are matched by NAME, in any order. This improves readability at the
# call site and makes intent explicit.

print(describe(age=25, city="Pune", name="Rohit"))   # same result

# Mixing rules:
#   * Positional arguments must come BEFORE keyword arguments.
#   * You cannot supply the same parameter twice.
#
# describe(name="Rohit", 25, "Pune")   # SyntaxError: positional after keyword

try:
    describe("Rohit", 25, city="Pune", name="Amit")
except TypeError as exc:
    print("TypeError:", exc)     # got multiple values for argument 'name'

try:
    describe("Rohit", 25, "Pune", country="India")
except TypeError as exc:
    print("TypeError:", exc)     # got an unexpected keyword argument 'country'

# INTERVIEW NOTE:
#   Keyword arguments are not just style - they let you skip optional
#   parameters and make boolean flags readable:
#   send_email(user, urgent=True)  is clearer than  send_email(user, True).


# ------------------------------------------------------------------------------
# 3. DEFAULT ARGUMENTS
# ------------------------------------------------------------------------------
# A default makes a parameter optional. If the caller omits it, the default is
# used. Parameters with defaults must come AFTER parameters without defaults.

def power(base, exponent=2):
    """Return base raised to exponent (default: square)."""
    return base ** exponent

print(power(5))                  # 25  (exponent defaults to 2)
print(power(5, 3))               # 125
print(power(5, exponent=3))      # 125

# You cannot put a required parameter after a defaulted one:
# def bad(a=1, b): ...           # SyntaxError: non-default argument follows default argument

# Defaults are evaluated ONCE, when the def statement executes.
# This is the single most important fact about defaults.

print("defining function ...")

def show_default(value, marker=[]):
    """Demonstrate that the default object is created once."""
    print("default id:", id(marker))
    return marker

show_default(1)
show_default(2)                  # same list object every call (same id)

# INTERVIEW: "Why is a mutable default argument dangerous?"
#
# def add_item(item, bucket=[]):
#     bucket.append(item)
#     return bucket
#
# The SAME list is reused across calls, so state leaks between calls.

def add_item_buggy(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add_item_buggy("a"))       # ['a']
print(add_item_buggy("b"))       # ['a', 'b']  <- leaked from the previous call!
print(add_item_buggy("c"))       # ['a', 'b', 'c']

# Proof: the default object is stored on the function object.
print(add_item_buggy.__defaults__)   # (['a', 'b', 'c'],)

# THE FIX: use None as a sentinel and create a fresh object inside.
def add_item(item, bucket=None):
    """Append item to bucket, creating a new list when none is given."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(add_item("a"))             # ['a']
print(add_item("b"))             # ['b']  <- fresh list each time

# The same trap applies to dicts, sets, and any mutable object.
def register_buggy(name, registry={}):
    registry[name] = True
    return registry

print(register_buggy("a"))       # {'a': True}
print(register_buggy("b"))       # {'a': True, 'b': True}  <- bug

# Immutable defaults are safe: int, str, tuple, frozenset, None, True/False.
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Rohit"))            # Hello, Rohit

# INTERVIEW FOLLOW-UP:
#   "But what if the caller WANTS a shared cache?"
#   Then make it explicit: a module-level cache, a class, or functools.lru_cache.
#   Do not hide shared state behind a default argument.

# INTERVIEW FOLLOW-UP:
#   "Are default values evaluated in the enclosing scope?"
#   Yes - at definition time. They cannot reference other parameters:
#   def f(a, b=a): ...  -> NameError at definition time.


# ------------------------------------------------------------------------------
# 4. POSITIONAL-ONLY PARAMETERS  ( / )
# ------------------------------------------------------------------------------
# PEP 570 (Python 3.8+). Everything BEFORE '/' can only be passed positionally.
# Useful when parameter names are an implementation detail, or to allow
# **kwargs to contain a key with the same name.

def divide(numerator, denominator, /):
    return numerator / denominator

print(divide(10, 2))             # 5.0

try:
    divide(numerator=10, denominator=2)
except TypeError as exc:
    print("TypeError:", exc)     # got some positional-only arguments passed as keyword arguments

# Built-in functions often behave this way (e.g. len(obj=...) is invalid).


# ------------------------------------------------------------------------------
# 5. KEYWORD-ONLY PARAMETERS  ( * )
# ------------------------------------------------------------------------------
# A bare '*' means: everything AFTER it must be passed by keyword.
# Great for boolean flags and for optional configuration.

def create_user(name, *, age, active=True):
    return {"name": name, "age": age, "active": active}

print(create_user("Rohit", age=25))                 # active defaults to True
print(create_user("Rohit", age=25, active=False))

try:
    create_user("Rohit", 25)
except TypeError as exc:
    print("TypeError:", exc)     # takes 1 positional argument but 2 were given

# Why keyword-only? This call is unreadable and easy to get wrong:
#   create_user("Rohit", 25, False)
# With '*', the caller must write active=False, which is self-documenting.


# ------------------------------------------------------------------------------
# 6. *args  -  VARIABLE-LENGTH POSITIONAL ARGUMENTS
# ------------------------------------------------------------------------------
# *args collects extra positional arguments into a TUPLE.
# The name 'args' is conventional, not special - '*values' works too.

def total(*numbers):
    """Return the sum of any number of numeric arguments."""
    print("received:", numbers, type(numbers))   # tuple
    return sum(numbers)

print(total())                   # 0
print(total(1, 2, 3))            # 6
print(total(*[1, 2, 3, 4]))      # 10  (unpacking at the call site)

# *args can be combined with normal parameters. Normal parameters take the
# leading positional arguments; the rest go into args.
def show_first(first, *rest):
    return first, rest

print(show_first(1, 2, 3))       # (1, (2, 3))

# Practical pattern: a logger or a wrapper that forwards anything.
def log_call(*args, **kwargs):
    print("args:", args, "kwargs:", kwargs)

log_call(1, 2, mode="fast")      # args: (1, 2) kwargs: {'mode': 'fast'}

# INTERVIEW NOTE:
#   *args is a tuple, so it is immutable and supports len(), indexing, unpacking.
#   Inside the function you can iterate it directly:
def average(*numbers):
    return sum(numbers) / len(numbers) if numbers else 0

print(average(10, 20, 30))       # 20.0


# ------------------------------------------------------------------------------
# 7. **kwargs  -  VARIABLE-LENGTH KEYWORD ARGUMENTS
# ------------------------------------------------------------------------------
# **kwargs collects extra keyword arguments into a DICT.
# Keys are always strings (they come from parameter names).

def build_profile(**fields):
    """Return a dict built from arbitrary keyword arguments."""
    print("received:", fields, type(fields))   # dict
    return fields

print(build_profile(name="Rohit", age=25, city="Pune"))
# {'name': 'Rohit', 'age': 25, 'city': 'Pune'}

# Unpack a dict at the call site with **.
details = {"name": "Rohit", "age": 25}
print(build_profile(**details))  # same dict

# Keys must be strings, otherwise TypeError.
try:
    build_profile(**{1: "x"})
except TypeError as exc:
    print("TypeError:", exc)     # keywords must be strings

# Duplicate keys between explicit and unpacked kwargs -> TypeError.
try:
    build_profile(name="Rohit", **{"name": "Amit"})
except TypeError as exc:
    print("TypeError:", exc)     # got multiple values for keyword argument 'name'


# ------------------------------------------------------------------------------
# 8. PUTTING IT ALL TOGETHER (ORDER MATTERS)
# ------------------------------------------------------------------------------
# Full signature grammar:
#
#   def f(pos_only, /, normal, default=1, *args, kw_only, kw_default=2, **kwargs):
#
# Order:
#   1. positional-only parameters        (before /)
#   2. normal parameters                 (may have defaults)
#   3. *args  (or bare * for keyword-only)
#   4. keyword-only parameters
#   5. **kwargs

def full_example(a, b=2, /, c=3, *args, d, e=5, **kwargs):
    """Show every parameter kind in one signature."""
    return {
        "a": a, "b": b, "c": c, "args": args,
        "d": d, "e": e, "kwargs": kwargs,
    }

print(full_example(1, 2, 3, 4, 5, d=6, f=7))
# {'a': 1, 'b': 2, 'c': 3, 'args': (4, 5), 'd': 6, 'e': 5, 'f': 7}

# Notice:
#   a, b are positional-only (before /)
#   c is normal (positional or keyword)
#   4, 5 go into args
#   d is keyword-only and REQUIRED
#   e is keyword-only with a default
#   f goes into kwargs

# INTERVIEW TIP:
#   You do not need to memorise the grammar, but you MUST know the precedence:
#   positional-only -> normal -> *args -> keyword-only -> **kwargs.


# ------------------------------------------------------------------------------
# 9. ARGUMENT UNPACKING AT THE CALL SITE
# ------------------------------------------------------------------------------
# * iterable  -> positional arguments
# ** mapping  -> keyword arguments
# This is the same '*' and '**' syntax as in the signature, but used in a CALL.

def point(x, y, z):
    return f"({x}, {y}, {z})"

coords = [1, 2, 3]
print(point(*coords))            # (1, 2, 3)

config = {"x": 1, "y": 2, "z": 3}
print(point(**config))           # (1, 2, 3)

# Unpacking also works in literals (Python 3.5+).
first = [1, 2]
second = [3, 4]
print([*first, *second])         # [1, 2, 3, 4]
print({**{"a": 1}, **{"b": 2}})  # {'a': 1, 'b': 2}

# * in a call requires an iterable; ** requires a mapping with string keys.
try:
    point(*5)
except TypeError as exc:
    print("TypeError:", exc)     # argument after * must be an iterable

# INTERVIEW NOTE:
#   f(*args) forwards positional arguments; f(**kwargs) forwards keyword
#   arguments. This is exactly how decorators preserve the wrapped signature.


# ------------------------------------------------------------------------------
# 10. INSPECTING A SIGNATURE (BONUS)
# ------------------------------------------------------------------------------
import inspect

def sample(a, b=2, *args, c, **kwargs):
    pass

sig = inspect.signature(sample)
print(sig)                       # (a, b=2, *args, c, **kwargs)
for name, param in sig.parameters.items():
    print(name, param.kind, param.default)
# a POSITIONAL_OR_KEYWORD <class 'inspect._empty'>
# b POSITIONAL_OR_KEYWORD 2
# args VAR_POSITIONAL <class 'inspect._empty'>
# c KEYWORD_ONLY <class 'inspect._empty'>
# kwargs VAR_KEYWORD <class 'inspect._empty'>


# ------------------------------------------------------------------------------
# 11. INTERVIEW GOTCHAS - QUICK REFERENCE
# ------------------------------------------------------------------------------
# Q: Positional vs keyword arguments?
# A: Positional match by order; keyword match by name. Positional must come first.
#
# Q: When are default arguments evaluated?
# A: Once, at function DEFINITION time - not on every call.
#
# Q: Why is def f(x, items=[]) dangerous?
# A: The same list is shared by every call. Use items=None then create a list.
#
# Q: *args vs **kwargs?
# A: *args -> tuple of extra positional arguments.
#    **kwargs -> dict of extra keyword arguments.
#
# Q: How do you forward arguments to another function?
# A: def wrapper(*args, **kwargs): return target(*args, **kwargs).
#
# Q: What does the bare * mean in a signature?
# A: Everything after it is keyword-only.
#
# Q: What does / mean in a signature?
# A: Everything before it is positional-only.
#
# Q: Can a function have both *args and **kwargs?
# A: Yes: def f(*args, **kwargs). Order is fixed: *args before **kwargs.
#
# Q: Can keyword arguments be passed in any order?
# A: Yes, after all positional arguments. Python matches them by name.
# ================================================================================
