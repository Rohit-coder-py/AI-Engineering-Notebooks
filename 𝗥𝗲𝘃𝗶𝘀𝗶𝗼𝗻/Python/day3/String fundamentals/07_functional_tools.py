"""
================================================================================
DAY 3 - B4. FUNCTIONAL TOOLS AND DOCUMENTATION
     lambda | higher-order functions | map | filter | sorted(key) | docstrings | type hints
================================================================================

INTERVIEW MINDSET
-----------------
Say: "Functions are first-class objects, so we can pass them to other
      functions and return them. lambda is a compact anonymous function for a
      SINGLE expression - useful as a key or callback, not for complex logic.
      map/filter return LAZY iterators in Python 3. sorted(key=...) is the
      idiomatic way to sort by a computed value."

Documentation and types are not decoration:
  * A docstring is the function's contract.
  * Type hints document intent and enable static analysis (mypy), but Python
    does NOT enforce them at runtime.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. LAMBDA FUNCTIONS
# ------------------------------------------------------------------------------
# Syntax: lambda parameters: expression
#   * Single EXPRESSION only - no statements, no assignments, no return keyword.
#   * The expression's value is returned automatically.
#   * Anonymous: it has no name unless you assign it.
#   * No annotations, no docstring.

square = lambda x: x * x
print(square(5))                 # 25

add = lambda a, b: a + b
print(add(2, 3))                 # 5

# Defaults and *args work:
greet = lambda name="world": f"hello {name}"
print(greet())                   # hello world
print(greet("Rohit"))            # hello Rohit

# lambda is most idiomatic INSIDE another call (as a key/callback).
pairs = [(1, "one"), (3, "three"), (2, "two")]
print(sorted(pairs, key=lambda p: p[1]))
# [(1, 'one'), (3, 'three'), (2, 'two')]  (sorted by the word)

# PEP 8: do not assign a lambda to a name - use def instead.
# BAD:  square = lambda x: x * x
# GOOD: def square(x): return x * x
# The def version has a name, a docstring, a traceback name, and is easier to test.

# Limitation demo: lambdas cannot contain statements.
# bad = lambda x: if x > 0: x   # SyntaxError

# INTERVIEW NOTE:
#   A lambda is still a function object: type(...) is <class 'function'>,
#   it supports __call__, and it can be passed anywhere a function is expected.
print(type(square))              # <class 'function'>


# ------------------------------------------------------------------------------
# 2. HIGHER-ORDER FUNCTIONS
# ------------------------------------------------------------------------------
# A higher-order function either:
#   (a) takes another function as an argument, or
#   (b) returns a function.
# map, filter, sorted, max, min are built-in examples of (a).

def apply(func, value):
    """Apply a one-argument function to a value."""
    return func(value)

print(apply(str.upper, "python"))    # PYTHON
print(apply(len, "python"))          # 6
print(apply(lambda n: n + 1, 41))    # 42

# Returning a function (factory / closure):
def make_power(exponent):
    """Return a function that raises its argument to exponent."""
    return lambda base: base ** exponent

square_fn = make_power(2)
cube_fn = make_power(3)
print(square_fn(5), cube_fn(2))      # 25 8

# Real-world use: strategy selection without long if/else chains.
def upper(text):
    return text.upper()

def lower(text):
    return text.lower()

def title(text):
    return text.title()

strategies = {"upper": upper, "lower": lower, "title": title}
print(strategies["title"]("hello world"))   # Hello World


# ------------------------------------------------------------------------------
# 3. map()
# ------------------------------------------------------------------------------
# map(func, iterable, ...) applies func to each item and returns a LAZY
# iterator in Python 3. Wrap it in list()/tuple()/sum() to consume it.
# With multiple iterables, it stops at the SHORTEST one.

numbers = [1, 2, 3, 4]

mapped = map(lambda n: n * 2, numbers)
print(type(mapped).__name__)     # map
print(list(mapped))              # [2, 4, 6, 8]

# The iterator is EXHAUSTED after one pass:
print(list(mapped))              # []  (nothing left)

# map with a named function is often clearer than a lambda.
print(list(map(str, numbers)))           # ['1', '2', '3', '4']
print(list(map(len, ["a", "bb", "ccc"])))   # [1, 2, 3]

# Multiple iterables:
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20])))   # [11, 22]

# map vs list comprehension:
#   map(func, xs)          -> concise for an existing function
#   [func(x) for x in xs]  -> more readable for expressions and filters
print([n * 2 for n in numbers])  # [2, 4, 6, 8]

# INTERVIEW NOTE:
#   In Python 2, map returned a list. In Python 3 it returns an iterator.
#   This is a favourite "what changed between Python 2 and 3" question.


# ------------------------------------------------------------------------------
# 4. filter()
# ------------------------------------------------------------------------------
# filter(predicate, iterable) keeps items for which predicate(item) is truthy.
# Returns a lazy iterator. filter(None, iterable) keeps TRUTHY items.

nums = [0, 1, 2, 3, 4, 5]

evens = filter(lambda n: n % 2 == 0, nums)
print(type(evens).__name__)      # filter
print(list(evens))               # [0, 2, 4]

# filter(None, ...) drops all falsy values: 0, "", None, [], {}, False.
mixed = [0, 1, "", "a", None, [], [1], False, True]
print(list(filter(None, mixed))) # [1, 'a', [1], True]

# Equivalent comprehension:
print([n for n in nums if n % 2 == 0])   # [0, 2, 4]

# INTERVIEW NOTE:
#   filter() cannot transform values - it only selects. Use map() or a
#   comprehension when you need both selection and transformation.


# ------------------------------------------------------------------------------
# 5. sorted() WITH key
# ------------------------------------------------------------------------------
# sorted(iterable, key=None, reverse=False) returns a NEW sorted list.
# key is a function applied to each element; sorting compares the RESULTS.
# The original iterable is never modified.

words = ["banana", "Apple", "cherry", "date"]
print(sorted(words))                       # ['Apple', 'banana', 'cherry', 'date']
print(sorted(words, key=len))              # ['date', 'Apple', 'banana', 'cherry']
print(sorted(words, key=str.lower))        # case-insensitive
print(sorted(words, key=len, reverse=True))# longest first
print(words)                               # original unchanged

# Sort records by a field:
students = [("Rohit", 85), ("Amit", 92), ("Sara", 78)]
print(sorted(students, key=lambda s: s[1]))
# [('Sara', 78), ('Rohit', 85), ('Amit', 92)]

# Highest score:
print(max(students, key=lambda s: s[1]))   # ('Amit', 92)

# Multiple sort criteria: return a TUPLE. Python compares tuples element-wise.
# Sort by score DESC, then name ASC.
print(sorted(students, key=lambda s: (-s[1], s[0])))
# [('Amit', 92), ('Rohit', 85), ('Sara', 78)]

# STABILITY: equal keys keep their original relative order.
records = [("b", 2), ("a", 2), ("c", 1)]
print(sorted(records, key=lambda r: r[1]))
# [('c', 1), ('b', 2), ('a', 2)]  <- b before a, as in the input

# itemgetter / attrgetter are faster and more readable than lambdas for fields.
from operator import itemgetter, attrgetter

print(sorted(students, key=itemgetter(1)))
# [('Sara', 78), ('Rohit', 85), ('Amit', 92)]

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def __repr__(self):
        return f"Student({self.name!r}, {self.score})"

people = [Student("Rohit", 85), Student("Amit", 92)]
print(sorted(people, key=attrgetter("score")))
# [Student('Rohit', 85), Student('Amit', 92)]

# sort() vs sorted():
#   list.sort()  -> in place, returns None, lists only.
#   sorted()     -> new list, any iterable, original untouched.
data = [3, 1, 2]
result = data.sort()
print(data, result)              # [1, 2, 3] None

# INTERVIEW NOTE:
#   Sorting is stable and O(n log n). A key function is called ONCE per item
#   (decorate-sort-undecorate), not on every comparison.


# ------------------------------------------------------------------------------
# 6. any(), all(), sum(), min(), max() WITH GENERATORS
# ------------------------------------------------------------------------------
# These short-circuit where possible and read well with generator expressions.

values = [2, 4, 6]
print(any(v > 5 for v in values))    # True
print(all(v % 2 == 0 for v in values))   # True

# all([]) is True and any([]) is False - empty-sequence edge cases.
print(all([]), any([]))              # True False

# min/max with key and default (default avoids ValueError on empty input):
print(max([], default=0))            # 0
print(min(words, key=len))           # date


# ------------------------------------------------------------------------------
# 7. functools.reduce() AND partial() (AWARENESS)
# ------------------------------------------------------------------------------
from functools import reduce, partial

# reduce(func, iterable, initial) folds left to right into ONE value.
print(reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0))   # 10
print(reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1))   # 24

# In modern Python, sum(), max(), min(), math.prod often replace reduce.
# reduce is still useful for custom folding logic.

# partial freezes some arguments, producing a new callable.
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(9))                 # 81

# INTERVIEW NOTE:
#   Know what reduce does and that it lives in functools. You rarely need it
#   in day-to-day code, but it appears in functional-programming questions.


# ------------------------------------------------------------------------------
# 8. DOCSTRINGS (PEP 257)
# ------------------------------------------------------------------------------
# First statement in a def/class/module. Triple-quoted. Stored in __doc__.
#
# One-line: imperative mood, ends with a period.
# Multi-line: summary line, blank line, details, then Args/Returns/Raises.

def normalize_name(name):
    """Return a trimmed, title-cased name.

    Args:
        name: Raw user input. Leading/trailing whitespace is ignored.

    Returns:
        The cleaned name. Returns an empty string for blank input.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    return name.strip().title()

print(normalize_name("  rohit  "))       # Rohit
print(normalize_name.__doc__.splitlines()[0])
# Return a trimmed, title-cased name.

# help(normalize_name) would render the docstring in the console.

# INTERVIEW NOTE:
#   A docstring documents the CONTRACT (inputs, outputs, errors) and WHY.
#   Comments explain WHY the implementation is written that way.
#   Good docstrings plus type hints are a strong signal in code reviews.


# ------------------------------------------------------------------------------
# 9. TYPE HINTS (FUNDAMENTALS)
# ------------------------------------------------------------------------------
# Annotations document expected types and power tools such as mypy, IDEs,
# and FastAPI. They are NOT enforced at runtime.

def repeat(text: str, times: int = 2) -> str:
    """Return text repeated times times."""
    return text * times

print(repeat("ab", 3))           # ababab
print(repeat(5, 2))              # 10  <- runs anyway; hints are not checks

# Annotations are stored in __annotations__ (evaluated lazily in 3.14+).
print(repeat.__annotations__)
# {'text': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}

# Common built-in generic types (3.9+):
#   list[int]              list of int
#   dict[str, int]         mapping str -> int
#   tuple[int, str]        fixed 2-tuple
#   tuple[int, ...]        variable-length tuple of int
#   set[str]               set of str
#   list[dict[str, int]]   nested

def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its length."""
    return {w: len(w) for w in words}

print(word_lengths(["a", "bb"]))     # {'a': 1, 'bb': 2}

# Optional values:
#   str | None            (Python 3.10+)
#   Optional[str]         (typing, older code)
def find_user(user_id: int) -> str | None:
    """Return a user name, or None when not found."""
    return None if user_id <= 0 else "Rohit"

print(find_user(-1))             # None

# Callables and Any:
from typing import Any, Callable

def apply_all(func: Callable[[int], int], values: list[int]) -> list[int]:
    """Apply func to every value."""
    return [func(v) for v in values]

print(apply_all(lambda n: n + 1, [1, 2]))   # [2, 3]

def log(message: str, **meta: Any) -> None:
    """Print a message with optional metadata."""
    print(message, meta)

log("started", attempt=1)

# Postponed evaluation (helps with forward references and import cycles):
#   from __future__ import annotations
# In 3.14 annotations are lazy by default (PEP 649), so this is less necessary.

# INTERVIEW NOTE:
#   "Are type hints enforced?" -> No, at runtime they are metadata. Use mypy /
#   pyright for static checking, or pydantic for runtime validation.
#   "Why use them?" -> Editor completion, refactoring safety, documentation,
#   and API schema generation.


# ------------------------------------------------------------------------------
# 10. INTERVIEW GOTCHAS - QUICK REFERENCE
# ------------------------------------------------------------------------------
# Q: lambda vs def?
# A: lambda is a single expression, anonymous, no docstring/annotations.
#    def is named, multi-statement, documentable, and preferred for reuse.
#
# Q: What does map() return in Python 3?
# A: A lazy iterator, not a list. Consume it with list()/sum()/etc.
#
# Q: map vs filter?
# A: map transforms every item; filter selects items by a predicate.
#
# Q: map vs list comprehension?
# A: Both work; comprehensions are usually more readable, map is concise when
#    you already have a function (e.g. map(str, xs)).
#
# Q: What does sorted(key=...) do?
# A: Calls key once per element and sorts by the returned values. Stable.
#
# Q: How do you sort by two fields?
# A: Return a tuple from key, e.g. key=lambda r: (r.age, r.name). Use negation
#    for descending numeric fields: (-r.score, r.name).
#
# Q: Difference between sort() and sorted()?
# A: sort() is in-place and returns None; sorted() returns a new list.
#
# Q: Why does a lambda in a loop return the same value?
# A: Closures capture variables, not values (late binding). Bind with a default
#    argument or a factory function.
#
# Q: Are type hints checked at runtime?
# A: No. They are metadata for tools and humans (unless a library enforces them).
# ================================================================================
