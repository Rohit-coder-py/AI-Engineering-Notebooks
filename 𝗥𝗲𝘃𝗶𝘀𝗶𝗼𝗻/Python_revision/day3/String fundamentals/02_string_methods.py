"""
================================================================================
DAY 3 - A2. COMMON STRING METHODS
================================================================================

INTERVIEW MINDSET
-----------------
Every str method returns a NEW string (or a list, or an int) - it NEVER
mutates the original, because str is immutable. Say that explicitly when an
interviewer asks "what does this method do to the string?"

Method families to recognise instantly:
  CASE      lower, upper, title, capitalize, swapcase, casefold
  TRIM      strip, lstrip, rstrip
  SPLIT     split, rsplit, splitlines, partition, rpartition
  JOIN      "sep".join(iterable_of_str)
  REPLACE   replace, translate, removeprefix, removesuffix
  SEARCH    find, rfind, index, rindex, count, startswith, endswith
  TEST      isalpha, isdigit, isalnum, isspace, isupper, islower, istitle
  LAYOUT    center, ljust, rjust, zfill, expandtabs
================================================================================
"""

text = "  Hello, Python World!  "

# ------------------------------------------------------------------------------
# 1. CASE CONVERSION
# ------------------------------------------------------------------------------
# lower() / upper()
#   Convert every cased character. Non-letters are unchanged.
#   Returns a new string; the original is untouched.

sentence = "Python is FUN"
print(sentence.lower())          # python is fun
print(sentence.upper())          # PYTHON IS FUN
print(sentence)                  # Python is FUN  (unchanged)

# title()
#   Uppercases the first letter of every WORD and lowercases the rest.
#   Word boundaries are non-letters, so apostrophes cause surprises.
print("hello world".title())     # Hello World
print("it's a test".title())     # It'S A Test   <- classic gotcha
print("hello-world".title())     # Hello-World
print("HELLO".title())           # Hello

# capitalize(): only the first character upper, everything else lower.
print("hELLO wORLD".capitalize())  # Hello world

# swapcase(): invert the case of every cased character.
print("PyThOn".swapcase())       # pYtHoN

# casefold(): aggressive lower-casing for CASELESS comparison.
# For ASCII, lower() and casefold() behave the same. For Unicode, casefold()
# handles special cases such as the German sharp s: "STRASSE" vs "straße".
print("STRASSE".casefold() == "straße".casefold())   # True
print("STRASSE".lower() == "straße".lower())         # False

# INTERVIEW: "lower() vs casefold()?"
#   lower()    -> simple lowercase mapping; use for display.
#   casefold() -> Unicode caseless matching; use for comparisons/search.
#   Neither is aware of Turkish locale rules (use locale-aware tooling if needed).


# ------------------------------------------------------------------------------
# 2. STRIPPING WHITESPACE (AND CHOSEN CHARACTERS)
# ------------------------------------------------------------------------------
# strip()   -> remove from BOTH ends
# lstrip()  -> left only
# rstrip()  -> right only
# With no argument: removes whitespace (space, \t, \n, \r, \f, \v).
# With an argument: removes ANY character in that set (not a prefix/suffix!).

messy = "   extra spaces   "
print(repr(messy.strip()))       # 'extra spaces'
print(repr(messy.lstrip()))      # 'extra spaces   '
print(repr(messy.rstrip()))      # '   extra spaces'

# Newlines and tabs count as whitespace too.
print(repr("\n\t data \t\n".strip()))   # 'data'

# The argument is a CHARACTER SET, not a substring.
print("xxhixx".strip("x"))       # hi
print("www.example.com".strip("cmowz."))   # example   <- watch out!
print("banana".strip("ab"))      # nan (stops at 'n', which is not in the set)

# Only the ENDS are affected; middle characters are never removed.
print("banana".strip("a"))       # banan

# INTERVIEW GOTCHA:
#   To remove a PREFIX/SUFFIX, use removeprefix()/removesuffix() (3.9+),
#   not strip().
print("file.txt".removesuffix(".txt"))   # file
print("unhappy".removeprefix("un"))      # happy


# ------------------------------------------------------------------------------
# 3. split() AND join() - THE MOST ASKED PAIR
# ------------------------------------------------------------------------------
# split(sep=None, maxsplit=-1)
#   * No argument: split on RUNS of whitespace and drop empty strings.
#   * With sep   : split on that exact separator and KEEP empty strings.
#   * maxsplit   : maximum number of splits; the remainder stays intact.

csv_line = "apple,banana,cherry"
print(csv_line.split(","))       # ['apple', 'banana', 'cherry']

spaced = "  Python   is    fun  "
print(spaced.split())            # ['Python', 'is', 'fun']  (whitespace runs)
print(spaced.split(" "))         # ['', '', 'Python', '', '', 'is', '', '', '', 'fun', '', '']

print("a,b,c,d".split(",", 2))   # ['a', 'b', 'c,d']   (only 2 splits)
print("a,b,c,d".rsplit(",", 2))  # ['a,b', 'c', 'd']   (split from the right)

# splitlines() splits on line boundaries and (by default) DROPS the newlines.
print("line1\nline2\r\nline3".splitlines())   # ['line1', 'line2', 'line3']
print("line1\nline2\n".splitlines())          # ['line1', 'line2']

# join(iterable_of_strings)
#   * Called on the SEPARATOR, not on the list.
#   * Every element must already be a str.
#   * Much faster than repeated '+' because it allocates once.

words = ["Python", "is", "fun"]
print(" ".join(words))           # Python is fun
print("-".join(["2026", "11", "21"]))   # 2026-11-21
print("".join(["a", "b", "c"]))         # abc

# join() with non-string items -> TypeError.
try:
    print(",".join([1, 2, 3]))
except TypeError as exc:
    print("TypeError:", exc)     # expected str instance, int found

# Fix with a generator expression - the idiomatic pattern.
numbers = [1, 2, 3]
print(",".join(str(n) for n in numbers))   # 1,2,3

# Round trip: split then join.
print("-".join("a b c".split()))           # a-b-c

# INTERVIEW: "How do you split a string into words and rebuild it?"
#   words = text.split(); rebuilt = " ".join(words).
#
# INTERVIEW: "Why is join() preferred over += in a loop?"
#   str is immutable: each += copies the whole accumulated string -> O(n^2).
#   join() computes the total length once and copies each piece once -> O(n).


# ------------------------------------------------------------------------------
# 4. replace()
# ------------------------------------------------------------------------------
# replace(old, new, count=-1) -> replace ALL occurrences by default.
# Matching is exact and case-sensitive; replacements are non-overlapping
# and processed left to right.

s = "I like cats. Cats are nice. cats!"
print(s.replace("cats", "dogs"))          # all lowercase occurrences only
print(s.replace("cats", "dogs", 1))       # first occurrence only
print(s.replace("Cats", "Dogs"))          # case-sensitive

# Non-overlapping semantics:
print("aaa".replace("aa", "b"))           # 'ba'  (not 'bb')
print("abab".replace("ab", "x"))          # 'xx'

# Remove characters by replacing with an empty string.
print("1,234,567".replace(",", ""))       # 1234567

# INTERVIEW NOTE:
#   replace() is O(n) per call and returns a new string.
#   For many single-character replacements, str.translate() is faster.
table = str.maketrans({"a": "4", "e": "3", "i": "1", "o": "0"})
print("elite".translate(table))           # 3l1t3


# ------------------------------------------------------------------------------
# 5. find() AND index() - SEARCHING
# ------------------------------------------------------------------------------
# find(sub[, start[, end]])   -> lowest index, or -1 if not found
# rfind(...)                  -> highest index, or -1
# index(...)                  -> like find, but raises ValueError if missing
# rindex(...)                 -> like rfind, but raises ValueError

quote = "to be or not to be"
print(quote.find("be"))          # 3
print(quote.rfind("be"))         # 16
print(quote.find("be", 4))       # 16  (search starts at index 4)
print(quote.find("xyz"))         # -1
print(quote.index("be"))         # 3

try:
    quote.index("xyz")
except ValueError as exc:
    print("ValueError:", exc)    # substring not found

# INTERVIEW RULE OF THUMB:
#   Use find() when "not found" is a normal outcome.
#   Use index() when absence is a bug you want to surface immediately.
#   To test presence only, use 'sub in text' - it reads better and is fast.

# start/end follow slice semantics: end is EXCLUSIVE.
print(quote.find("be", 0, 3))    # -1  (index 3 is outside [0, 3))

# Searching from the end, then checking the result, is the classic
# "find the last word" pattern.
last_space = quote.rfind(" ")
print(quote[last_space + 1:])    # be


# ------------------------------------------------------------------------------
# 6. count()
# ------------------------------------------------------------------------------
# count(sub[, start[, end]]) counts NON-OVERLAPPING occurrences.

print("banana".count("a"))       # 3
print("banana".count("na"))      # 2
print("aaa".count("aa"))         # 1  (non-overlapping)
print("aaaa".count("aa"))        # 2
print("banana".count("a", 2))    # 2  (from index 2)
print("banana".count("a", 0, 3)) # 1  (end exclusive)

# Empty substring: len(text) + 1 matches (one before every character + end).
print("abc".count(""))           # 4

# INTERVIEW NOTE:
#   count("") is a deliberate edge case. Mention it if asked about edge cases.
#   For character frequency, collections.Counter is usually clearer.


# ------------------------------------------------------------------------------
# 7. startswith() AND endswith()
# ------------------------------------------------------------------------------
# Both accept a TUPLE of options - very useful for file-extension checks.
# Optional start/end arguments follow slice rules.

filename = "report_2026.pdf"
print(filename.startswith("report"))       # True
print(filename.endswith(".pdf"))           # True
print(filename.endswith((".csv", ".xlsx")))  # False
print(filename.startswith(("img_", "report_")))  # True

print(filename.startswith("2026", 7))      # True (start searching at index 7)
print(filename.endswith("report", 0, 6))   # True (end exclusive)

# These are PREFIX/SUFFIX tests, not membership tests.
print("bc" in "abc")                       # True  (substring anywhere)
print("abc".startswith("bc"))              # False (not at the start)

# INTERVIEW: "How do you check many possible prefixes?"
#   Use a tuple: name.startswith(("Mr.", "Ms.", "Dr.")).
#   Do not write a chain of 'or' comparisons.


# ------------------------------------------------------------------------------
# 8. OTHER USEFUL METHODS (KNOW THEY EXIST)
# ------------------------------------------------------------------------------

# partition(sep) -> (before, sep, after); always a 3-tuple.
print("user@example.com".partition("@"))   # ('user', '@', 'example.com')
print("no-sep".partition("@"))             # ('no-sep', '', '')

# is* tests return bool and are often used for validation.
print("abc".isalpha())           # True
print("123".isdigit())           # True
print("abc123".isalnum())        # True
print("   ".isspace())           # True
print("HELLO".isupper())         # True
print("hello".islower())         # True
print("Hello World".istitle())   # True
print("".isalpha())              # False (empty string is not alpha)

# Numeric subtleties (great edge-case interview material):
print("123".isdigit())           # True
print("²".isdigit())             # True  (superscript two)
print("²".isdecimal())           # False
print("²".isnumeric())           # True
# Rule of thumb: isdecimal() is the safest check before int().

# Layout helpers.
print("42".zfill(5))             # 00042
print("-42".zfill(5))            # -0042 (sign aware)
print("hi".center(10, "-"))      # ----hi----
print("hi".ljust(6, "."))        # hi....
print("hi".rjust(6, "."))        # ....hi

# expandtabs: replace \t with spaces (default tabsize 8).
print("a\tb".expandtabs(4))      # "a   b"

# Encoding / decoding (bridge between str and bytes).
encoded = "cafe".encode("utf-8")
print(encoded.hex())             # 63616665
print(encoded.decode("utf-8"))   # cafe


# ------------------------------------------------------------------------------
# 9. METHOD CHEAT-SHEET FOR INTERVIEWS
# ------------------------------------------------------------------------------
# QUESTION                         METHOD / ANSWER
# Remove leading/trailing spaces   s.strip()
# Remove only trailing newline     s.rstrip("\n")
# Split a CSV line                 s.split(",")
# Split on any whitespace          s.split()
# Join words with spaces           " ".join(words)
# Replace a substring              s.replace(old, new[, count])
# Find position or -1              s.find(sub)
# Find position or ValueError      s.index(sub)
# Count occurrences                s.count(sub)  (non-overlapping)
# Check prefix/suffix              s.startswith(tuple) / s.endswith(tuple)
# Case-insensitive compare         a.casefold() == b.casefold()
# Remove a known prefix            s.removeprefix(p)  (3.9+)
# Format a number                  f"{x:.2f}"
#
# REMEMBER: none of these mutate the original string.
# ================================================================================
