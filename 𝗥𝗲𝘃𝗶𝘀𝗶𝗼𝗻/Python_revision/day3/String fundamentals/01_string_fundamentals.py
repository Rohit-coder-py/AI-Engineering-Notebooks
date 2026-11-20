"""
================================================================================
DAY 3 - A1. STRING FUNDAMENTALS
================================================================================

INTERVIEW MINDSET
-----------------
Do NOT say: "A string is a list of characters."

DO say:     "A str is an IMMUTABLE sequence of Unicode code points.
             It supports the sequence protocol (indexing, slicing, len(),
             iteration, membership) but it is not a list - it cannot be
             mutated in place. Indexing returns a NEW one-character string,
             because Python has no separate 'char' type."

Why interviewers care:
  * Immutability  -> strings are HASHABLE -> valid dict keys / set members.
  * Sequence rules -> slicing behaves exactly like list / tuple / range.
  * Unicode       -> len() counts code points, not bytes and not glyphs.
  * Performance   -> repeated '+' in a loop is O(n^2); join() is O(n).
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. STRING CREATION
# ------------------------------------------------------------------------------
# A string literal can use single quotes, double quotes, or triple quotes.
# There is no semantic difference between ' and " - choose one and be consistent.

empty = ""
single = 'Python'
double = "Python"
print(single == double)          # True  - same characters, same value

# Triple quotes: multi-line text and docstrings.
paragraph = """Python is readable.
Readability counts."""
print(paragraph)
print(len(paragraph))            # 39 (includes the newline character)

# Adjacent literals are concatenated by the COMPILER (no '+' needed).
# Useful for long messages; must be literals, not variables.
message = ("This is one long "
           "sentence built from "
           "adjacent literals.")
print(message)                   # This is one long sentence built from adjacent literals.

# Convert other objects to str with str().
number_as_text = str(42)
print(number_as_text, type(number_as_text))   # 42 <class 'str'>

# Build a string from an iterable of strings with join().
from_parts = "".join(["P", "y", "t", "h", "o", "n"])
print(from_parts)                # Python

# Bytes are NOT str. Decode bytes -> str; encode str -> bytes.
raw_bytes = b"caf\xc3\xa9"       # UTF-8 encoding of "cafe" with an accent
decoded = raw_bytes.decode("utf-8")
print(len(raw_bytes), len(decoded))   # 5 4  (bytes vs code points)

# INTERVIEW NOTE:
#   str  = text  (Unicode code points)
#   bytes = raw data (0-255 values)
#   Mixing them raises TypeError: can only concatenate str (not "bytes") to str.


# ------------------------------------------------------------------------------
# 2. INDEXING (POSITIVE AND NEGATIVE)
# ------------------------------------------------------------------------------
# Indexing is 0-based. Negative indexes count from the end: -1 is the last item.
#
#        P    y    t    h    o    n
#   +    0    1    2    3    4    5
#   -   -6   -5   -4   -3   -2   -1

word = "Python"

print(word[0])                   # P
print(word[5])                   # n
print(word[-1])                  # n   (last character)
print(word[-6])                  # P   (first character)

# Each index returns a NEW string of length 1 - there is no 'char' type.
first_char = word[0]
print(type(first_char), len(first_char))   # <class 'str'> 1

# Out-of-range indexing raises IndexError (it does NOT wrap around).
try:
    print(word[6])
except IndexError as exc:
    print("IndexError:", exc)    # string index out of range

# len() is O(1): the length is stored on the string object.
print(len(word))                 # 6

# Strings are iterable, so they work with for loops and comprehensions.
for ch in "abc":
    print(ch, end=" ")           # a b c
print()

# Unpacking works like any sequence (number of names must match).
a, b, c = "xyz"
print(a, b, c)                   # x y z


# ------------------------------------------------------------------------------
# 3. SLICING  ->  s[start:stop:step]
# ------------------------------------------------------------------------------
# Rules that interviewers test:
#   * start is INCLUSIVE, stop is EXCLUSIVE.
#   * Any part may be omitted.
#   * Out-of-range slice bounds are CLAMPED - no IndexError.
#   * step defaults to 1; a negative step walks backwards.
#   * Slicing always returns a NEW string (even a full copy).

s = "Python"

print(s[1:4])                    # yth   (indexes 1, 2, 3)
print(s[:3])                     # Pyt   (from the beginning)
print(s[3:])                     # hon   (to the end)
print(s[:])                      # Python (full shallow copy)
print(s[::2])                    # Pto   (every 2nd character)
print(s[1::2])                   # yhn   (start at 1, every 2nd)
print(s[::-1])                   # nohtyP (reverse)
print(s[-3:])                    # hon   (last three)
print(s[:-3])                    # Pyt   (everything except last three)
print(s[-4:-1])                  # tho
print(s[10:20])                  # ''    (clamped, not an error)
print(s[4:1])                    # ''    (start > stop with positive step)

# A slice object can be stored and reused.
last_three = slice(-3, None)
print(s[last_three])             # hon

# Reversing a string: s[::-1] is the idiomatic interview answer.
# reversed(s) also works but returns an iterator, not a string:
print("".join(reversed(s)))      # nohtyP

# COMMON MISTAKE: slicing does not mutate the original.
t = "hello"
t[1:3]                           # evaluates to "el" but is discarded
print(t)                         # hello

# INTERVIEW NOTE:
#   s[start:stop:step] is implemented by calling s.__getitem__(slice(...)).
#   Slicing is O(k) in the length of the result, not O(n) of the original.


# ------------------------------------------------------------------------------
# 4. STRING IMMUTABILITY
# ------------------------------------------------------------------------------
# str objects cannot be modified after creation. Any "change" creates a new
# string object and rebinds the name to it.

name = "rohit"
try:
    name[0] = "R"
except TypeError as exc:
    print("TypeError:", exc)     # 'str' object does not support item assignment

# The correct way: build a new string and rebind.
name = "R" + name[1:]
print(name)                      # Rohit

# id() shows the object identity. Rebinding usually changes the id.
original = "data"
before = id(original)
original = original + " science"
print(id(original) == before)    # False (normally)

# NUANCE: CPython may optimise 's += t' by resizing in place when the string's
# reference count is 1. Logically it is still a NEW value, so never rely on
# id() to prove immutability in an interview - explain the LANGUAGE rule.

# Why immutability is a feature:
#   1) Hashable -> safe dict keys and set elements (hash cannot change).
#   2) Safe sharing -> passing a string to a function cannot corrupt the caller.
#   3) Thread-friendly -> immutable data needs no locking.
#   4) Interning -> identical literals can share one object -> fast equality.

# Small strings / identifier-like literals are often INTERNED (shared).
x = "hello"
y = "hello"
print(x == y, x is y)            # True True (CPython, implementation detail)

# NEVER use 'is' to compare string VALUES. 'is' compares identity.
# Use == (value equality). CPython may also emit a SyntaxWarning for
# literal 'is' comparisons in newer versions.

# Rebuilding a string character by character:
#   BAD  (O(n^2)):  result = ""; for ch in text: result += ch
#   GOOD (O(n))  :  result = "".join(parts)
parts = ["P", "y", "t", "h", "o", "n"]
print("-".join(parts))           # P-y-t-h-o-n

# INTERVIEW FOLLOW-UP:
#   "If strings are immutable, why does s += 'x' work?"
#   Because += on an immutable type is REASSIGNMENT: s = s + 'x'.
#   A new string is produced and s is rebound. The old object is unchanged.


# ------------------------------------------------------------------------------
# 5. CONCATENATION AND REPETITION
# ------------------------------------------------------------------------------
# +  concatenates (both operands MUST be str)
# *  repeats (str * int, or int * str)

first = "Ada"
last = "Lovelace"
full_name = first + " " + last
print(full_name)                 # Ada Lovelace

line = "-" * 30
print(line)                      # ------------------------------
print("=" * 3 + " OK " + "=" * 3)  # === OK ===

# Repetition with 0 or a negative count gives an empty string.
print(repr("hi" * 0))            # ''
print(repr("hi" * -2))           # ''

# Type errors: str + int is NOT implicit conversion.
try:
    print("Age: " + 25)
except TypeError as exc:
    print("TypeError:", exc)     # can only concatenate str (not "int") to str

# Fix with an explicit conversion or an f-string.
print("Age: " + str(25))         # Age: 25
print(f"Age: {25}")              # Age: 25

# PERFORMANCE TRAP (very common interview question):
#   In a loop, + creates a new string each iteration -> O(n^2) copying.
#   Use a list + "".join(...) -> O(n).
words = ["Python", "is", "fun"]
sentence = " ".join(words)
print(sentence)                  # Python is fun

# INTERVIEW NOTE:
#   "".join(iterable) requires every element to be a str.
try:
    print(",".join([1, 2, 3]))
except TypeError as exc:
    print("TypeError:", exc)     # sequence item 0: expected str instance, int found


# ------------------------------------------------------------------------------
# 6. STRING FORMATTING
# ------------------------------------------------------------------------------
# Three generations of formatting exist in Python:
#   1) % formatting          (oldest, C-style, still common in logging)
#   2) str.format()          (Python 2.6+)
#   3) f-strings             (Python 3.6+, recommended for new code)
#
# All three produce a NEW string; none mutate the template.

# ---------- 6a. f-strings (PREFERRED) ----------
name = "Rohit"
age = 25
score = 91.5678

print(f"Name: {name}, Age: {age}")            # Name: Rohit, Age: 25
print(f"Next year: {age + 1}")                # expressions are allowed
print(f"Score: {score:.2f}")                  # 91.57  (2 decimal places)
print(f"Score: {score:10.2f}")                # right-aligned in width 10
print(f"Score: {score:<10.2f}|")              # left-aligned
print(f"Score: {score:^10.2f}|")              # centered
print(f"Padded: {42:05d}")                    # 00042  (zero-padded integer)
print(f"Thousands: {1234567:,}")              # 1,234,567
print(f"Percent: {0.873:.1%}")                # 87.3%
print(f"Hex: {255:#x}")                       # 0xff
print(f"Bool: {True}")                        # True

# Conversion flags: !r (repr), !s (str), !a (ascii)
print(f"{name!r}")                            # 'Rohit'
print(f"{name!s}")                            # Rohit

# Self-documenting expressions (Python 3.8+): handy for debugging.
print(f"{age=}")                              # age=25

# Nested fields: dynamic width / precision.
width = 8
precision = 3
print(f"{3.14159:{width}.{precision}f}")      # "   3.142"

# Format spec grammar (memorise the order):
#   [[fill]align][sign][#][0][width][grouping][.precision][type]
#   align: < left, > right, ^ center, = pad after sign
#   type : d int, f float, e scientific, % percent, s str, x/X hex, b binary

# ---------- 6b. str.format() ----------
print("Name: {}, Age: {}".format(name, age))          # positional
print("Name: {0}, Age: {1}".format(name, age))        # explicit positions
print("{0} {0} {1}".format("hi", "there"))            # reuse an argument
print("Name: {n}, Age: {a}".format(n=name, a=age))    # named fields
print("{:>10.2f}".format(score))                      # format spec works too
print("{name!r}".format(name=name))                   # conversion flags

# format() is still useful when the template is DATA (loaded from a file or DB)
# rather than a literal in the source code, because f-strings need source text.

# ---------- 6c. % formatting (legacy) ----------
print("Name: %s, Age: %d" % (name, age))              # Name: Rohit, Age: 25
print("Score: %.2f" % score)                          # Score: 91.57
print("%(n)s is %(a)d" % {"n": name, "a": age})       # mapping form
print("%r" % name)                                    # repr
print("%05d" % 42)                                    # 00042

# Gotcha: a single argument can be a tuple-looking value.
print("Value: %s" % (42,))       # correct - tuple with one item
# print("Value: %s" % 42)        # also works for a single non-tuple value

# ---------- 6d. Which one should you use? ----------
#   f-strings  : default choice; fastest and most readable.
#   format()   : dynamic templates, reused format strings.
#   %          : legacy code and some logging patterns
#                (logging uses %-style LAZILY: logger.info("x=%s", x)).
#
# INTERVIEW NOTE:
#   f-strings are evaluated IMMEDIATELY when the line runs.
#   Logging's %-style is evaluated ONLY if the log level is enabled - that is
#   why logging prefers lazy %-style over eagerly built f-strings.


# ------------------------------------------------------------------------------
# 7. INTERVIEW GOTCHAS - QUICK REFERENCE
# ------------------------------------------------------------------------------
# Q: Is a string mutable?
# A: No. Index/slice assignment raises TypeError. "Changes" create new objects.
#
# Q: What does s[-1] return?
# A: The last character, as a new 1-character string.
#
# Q: What does s[100:200] do?
# A: Returns '' - slices clamp, they never raise IndexError.
#
# Q: Difference between s[0] and s[0:1]?
# A: Both give a 1-character string; the second is a slice and returns a copy.
#
# Q: Why are strings hashable?
# A: Because they are immutable, so their hash never changes during their life.
#
# Q: Is 'is' safe for string comparison?
# A: No. Use ==. 'is' checks object identity and depends on interning.
#
# Q: How do you reverse a string?
# A: s[::-1]. For an iterator: "".join(reversed(s)).
#
# Q: How do you build a large string efficiently?
# A: Collect parts in a list and call "".join(parts) once - O(n), not O(n^2).
#
# Q: Difference between str and bytes?
# A: str holds Unicode code points; bytes holds raw 0-255 values. Use
#    encode()/decode() with an explicit encoding (normally UTF-8).
# ================================================================================
