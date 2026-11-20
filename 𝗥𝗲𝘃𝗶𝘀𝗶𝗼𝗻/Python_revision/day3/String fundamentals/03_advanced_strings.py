"""
================================================================================
DAY 3 - A3. OTHER STRING CONCEPTS
     Membership | Escape characters & raw strings | Comparison | Unicode
================================================================================

INTERVIEW MINDSET
-----------------
Strings look simple, but most "gotcha" interview questions live here:
  * 'in' is a SUBSTRING test, not a word test.
  * A raw string changes how the LEXER reads backslashes, not the value at runtime.
  * String comparison is LEXICOGRAPHIC BY CODE POINT, not alphabetical-by-locale.
  * len() counts CODE POINTS - not bytes, not visible characters.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. STRING MEMBERSHIP  ->  substring in string
# ------------------------------------------------------------------------------
# 'sub in text' returns True if sub appears ANYWHERE in text.
# It is case-sensitive and does not respect word boundaries.

text = "The quick brown fox jumps over the lazy dog"

print("quick" in text)           # True
print("Quick" in text)           # False (case-sensitive)
print("fox" in text)             # True
print("cat" in text)             # False
print("" in text)                # True  (empty string is in every string)

# The right operand of 'in' must be a string (or an object supporting __contains__).
# 'in' on a dict checks KEYS; on a list/tuple/set it checks ELEMENTS.
print("quick" in text.split())   # True  - word-level check
print("qui" in text.split())     # False - "qui" is not a whole word

# Word-boundary check without regex (simple approach):
words = text.lower().split()
print("the" in words)            # True
print("he" in words)             # False

# Negation reads naturally:
if "python" not in text.lower():
    print("no mention of python")   # runs

# Complexity: substring search is not a single hash lookup. CPython uses an
# efficient two-way algorithm, but conceptually think "scan", not O(1).
# Membership in a set of words IS average O(1); use that when checking many words.

# INTERVIEW GOTCHA:
#   "is 'ana' in 'banana'?" -> True (substring).
#   "Does 'banana' contain the WORD 'ana'?" -> depends on tokenisation.

# To find ALL positions, loop with str.find and advance past each match.
haystack = "abababa"
needle = "aba"
positions = []
start = 0
while True:
    pos = haystack.find(needle, start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1          # +1 allows overlapping matches
print(positions)             # [0, 2, 4]


# ------------------------------------------------------------------------------
# 2. ESCAPE CHARACTERS
# ------------------------------------------------------------------------------
# A backslash introduces an escape sequence that represents a special character.
#
#   \n   newline              \t   tab                 \r   carriage return
#   \\   literal backslash    \'   single quote        \"   double quote
#   \b   backspace            \f   form feed           \v   vertical tab
#   \0   null character       \a   bell
#   \xhh      character from 2 hex digits      e.g. \x41 -> 'A'
#   \ooo      character from 3 octal digits    e.g. \101 -> 'A'
#   \uXXXX    Unicode code point, 4 hex digits e.g. \u00e9 -> 'e' with acute
#   \UXXXXXXXX Unicode code point, 8 hex digits e.g. \U0001F600 -> emoji
#   \N{NAME}  Unicode character by official name
#   \<newline> line continuation (the newline is removed)

print("line1\nline2")            # two lines
print("col1\tcol2")              # tab-separated
print("C:\\Users\\rohit")        # C:\Users\rohit
print("She said \"hi\"")         # She said "hi"
print("It\'s fine")              # It's fine
print("\x41\x42\x43")            # ABC
print("\101\102\103")            # ABC
print(ord("\u00e9"))             # 233  (avoid printing non-ASCII when unsure)
print(ord("\U0001F600"))         # 128512

# Unknown escapes (for example "\d") are currently kept literally, but
# Python 3.12+ raises a SyntaxWarning and they may become errors. Escape the
# backslash explicitly or use a raw string.
print(repr("\\d"))               # '\\d'  (explicit backslash + d)

# A backslash at the end of a line continues the logical line.
total = 1 + 2 + \
        3 + 4
print(total)                     # 10

# INTERVIEW NOTE:
#   '\n' is ONE character at runtime, even though it is written with two
#   characters in source code. len("\n") == 1.


# ------------------------------------------------------------------------------
# 3. RAW STRINGS  r"..."
# ------------------------------------------------------------------------------
# A raw string tells the PARSER not to interpret backslash escapes.
# The backslashes stay in the value exactly as typed.
# Very common for regular expressions and Windows paths.

normal = "C:\new\table"          # \n = newline, \t = tab  (wrong!)
raw = r"C:\new\table"            # literal backslashes      (correct)

print(repr(normal))              # 'C:\new\table' - escapes show the REAL newline/tab
print(repr(raw))                 # 'C:\\new\\table'
print(len(normal), len(raw))     # 10 12

print(r"\n")                     # prints backslash + n, not a newline
print(len(r"\n"))                # 2

# Raw strings are still strings: methods, indexing, slicing all work.
print(r"abc\def"[0])             # a

# LIMITATIONS (favourite interview follow-ups):
#   1) A raw string cannot END with an odd number of backslashes.
#      r"abc\"  -> SyntaxError (the backslash escapes the closing quote).
#      Workaround: r"abc" + "\\"  or use a normal string.
#   2) Raw strings do not disable quote escaping:
#      r"\"" is a valid string containing a backslash and a quote.
#   3) Raw strings do not make regex "safe" - you still need to understand
#      regex escaping. They simply avoid DOUBLE escaping.

import re
pattern = r"\d+\.\d+"            # regex: digits, dot, digits
print(re.findall(pattern, "pi=3.14 and e=2.71"))   # ['3.14', '2.71']

# f-strings and raw strings can be combined: rf"..." (or fr"...").
name = "rohit"
print(rf"path\{name}\file")      # path\rohit\file  (braces still interpolate)

# INTERVIEW ONE-LINER:
#   "A raw string affects LEXING, not the runtime type. It is still a str."


# ------------------------------------------------------------------------------
# 4. STRING COMPARISON
# ------------------------------------------------------------------------------
# Strings compare LEXICOGRAPHICALLY by Unicode code point:
#   compare the first differing character; if one string is a prefix of the
#   other, the shorter string is smaller.
# This is NOT dictionary/alphabetical order for mixed case or accents.

print("apple" < "banana")        # True   (a < b)
print("apple" < "apricot")       # True   (p == p, p < r)
print("app" < "apple")           # True   (prefix is smaller)
print("apple" == "apple")        # True
print("apple" != "Apple")        # True

# Case matters because uppercase letters have LOWER code points than lowercase.
print(ord("A"), ord("a"))        # 65 97
print("Z" < "a")                 # True
print("Apple" < "apple")         # True
print(sorted(["banana", "Apple", "cherry"]))
# ['Apple', 'banana', 'cherry']  <- uppercase sorts first

# Numeric strings do NOT compare numerically.
print("10" < "9")                # True  ('1' < '9')
print(int("10") < int("9"))      # False

# Case-insensitive comparison: casefold() both sides (best for Unicode).
a = "Hello"
b = "HELLO"
print(a == b)                    # False
print(a.casefold() == b.casefold())   # True

# Or compare with a key, e.g. for sorting:
names = ["charlie", "Alice", "bob"]
print(sorted(names, key=str.casefold))   # ['Alice', 'bob', 'charlie']

# Equality (==) vs identity (is) - a classic trap.
x = "hello"
y = "hello"
print(x == y)                    # True  - same value
print(x is y)                    # True  - CPython interning (implementation detail)

y = "hel" + "lo"                 # computed at runtime
print(x == y)                    # True
print(x is y)                    # usually False - do not rely on this

# INTERVIEW RULE:
#   == compares VALUE. 'is' compares OBJECT IDENTITY. Use == for strings,
#   always. 'is' is for None / True / False / sentinels.
#
# Comparing str with int using == is simply False (no error),
# but ORDERING comparisons raise TypeError:
try:
    print("5" < 5)
except TypeError as exc:
    print("TypeError:", exc)     # '<' not supported between 'str' and 'int'

# INTERVIEW NOTE:
#   There is no locale-aware collation in plain Python comparison.
#   For human-language sorting, use locale.strxfrm or a library such as PyICU.


# ------------------------------------------------------------------------------
# 5. BASIC UNICODE AWARENESS
# ------------------------------------------------------------------------------
# Python 3 str = sequence of Unicode CODE POINTS (not UTF-8 bytes).
# Each code point is an integer 0..0x10FFFF. ord()/chr() convert between them.

print(ord("A"))                  # 65
print(chr(65))                   # A
print(hex(ord("A")))             # 0x41

# len() counts CODE POINTS.
print(len("abc"))                # 3
print(len("\u00e9"))             # 1  (precomposed e-acute)
print(len("e\u0301"))            # 2  (e + COMBINING ACUTE ACCENT)

# Encoding turns str into bytes. UTF-8 uses 1-4 bytes per code point.
text_unicode = "caf\u00e9"
encoded = text_unicode.encode("utf-8")
print(len(text_unicode), len(encoded))   # 4 5  (the accent takes 2 bytes)
print(encoded.hex())                     # 636166c3a9

# Decoding turns bytes back into str.
print(encoded.decode("utf-8") == text_unicode)   # True

# Wrong encoding -> UnicodeDecodeError. Handle errors explicitly.
bad = b"caf\xe9"                 # latin-1 encoded
try:
    bad.decode("utf-8")
except UnicodeDecodeError as exc:
    print("UnicodeDecodeError:", exc.reason)   # unexpected end of data

print(ascii(bad.decode("latin-1")))   # 'caf\xe9' (correct for latin-1)
# Use ascii() so the replacement character prints safely on any console.
print(ascii(bad.decode("utf-8", errors="replace")))   # 'caf\ufffd'
print(ascii(bad.decode("utf-8", errors="ignore")))    # 'caf'

# Normalisation: visually identical text can have different code points.
import unicodedata

nfc = unicodedata.normalize("NFC", "e\u0301")   # composed
nfd = unicodedata.normalize("NFD", "\u00e9")    # decomposed
print(len(nfc), len(nfd))        # 1 2
print(nfc == nfd)                # False - different code point sequences
print(unicodedata.normalize("NFC", nfd) == nfc)   # True

# For user-facing comparisons, normalise first:
#   unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b)

# Emoji and grapheme clusters:
#   len() counts code points, but one visible glyph may use several code points
#   (skin tone modifiers, ZWJ sequences, flags, combining marks).
family = "\U0001F468\u200D\U0001F469\u200D\U0001F467"   # man+ZWJ+woman+ZWJ+girl
print(len(family))               # 5 code points, 1 visible emoji sequence

# Reversing by code point can BREAK grapheme clusters:
#   "\U0001F468\u200D..."[::-1] is not a valid family emoji.
#   For production text handling, use a grapheme-aware library.

# Useful helpers:
print("abc".isascii())           # True
print("\u00e9".isascii())        # False
print(ascii("\u00e9"))           # "'\\xe9'"  (ASCII-only repr)

# INTERVIEW SUMMARY:
#   * Python 3 str is Unicode text; bytes are raw data.
#   * UTF-8 is an ENCODING of Unicode, not a separate string type.
#   * len(str) = code points; len(str.encode("utf-8")) = bytes.
#   * Normalise (NFC) before comparing user input.
#   * Use casefold() for caseless matching.
# ================================================================================
