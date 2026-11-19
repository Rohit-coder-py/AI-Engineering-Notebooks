"""
DAY 1 | 03 - TYPE CONVERSION (casting)
====================================
Implicit (automatic) vs explicit (manual) conversion, common failures,
safe conversion with try/except.

Run: python 03_type_conversion.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. IMPLICIT CONVERSION (type promotion)")
# ----------------------------------------------------------------------
# Python promotes in numeric expressions: bool -> int -> float -> complex
print(1 + 2.0, type(1 + 2.0))           # float
print(True + 1, type(True + 1))         # int
print(1 + 2j, type(1 + 2j))             # complex
# NO implicit conversion between str and numbers:
try:
    "3" + 4
except TypeError as e:
    print("TypeError:", e)

# ----------------------------------------------------------------------
section("2. EXPLICIT: int(), float(), str(), bool()")
# ----------------------------------------------------------------------
print(int("42"), int(3.99), int(-3.99), int(True))  # int() TRUNCATES toward zero
print(float("3.14"), float(5), float("1e3"))
print(str(100), str(3.5), str([1, 2]), str(None))
print(bool(0), bool(""), bool("0"), bool([]), bool([0]))

# Failures
for bad in ["3.5", "abc", "", " 7 "]:
    try:
        print(f"int({bad!r}) =", int(bad))
    except ValueError as e:
        print(f"int({bad!r}) -> ValueError: {e}")
# Note: int(" 7 ") works - whitespace is stripped.
# To convert "3.5" to int: int(float("3.5")) -> 3

# ----------------------------------------------------------------------
section("3. BASE CONVERSION")
# ----------------------------------------------------------------------
print(int("1010", 2), int("ff", 16), int("17", 8))
print(bin(10), oct(15), hex(255))
print(format(10, "b"), format(255, "X"), f"{10:08b}")

# ----------------------------------------------------------------------
section("4. CHARACTER <-> NUMBER")
# ----------------------------------------------------------------------
print(ord("A"), chr(65), ord("a") - ord("A"))
print(chr(ord("a") + 2))  # caesar-shift building block

# ----------------------------------------------------------------------
section("5. CONTAINER CONVERSIONS")
# ----------------------------------------------------------------------
print(list("abc"), list((1, 2)), list({1, 2}), list({"a": 1}))   # dict -> keys
print(tuple([1, 2, 2]), set([1, 2, 2, 3]), frozenset([1, 2]))
print(dict([("a", 1), ("b", 2)]), dict(zip("abc", [1, 2, 3])))
print(list(range(5)), list(map(int, "12345")))
print("".join(["a", "b"]), "-".join(map(str, [1, 2, 3])))
# list <-> str is a split/join job, not a cast:
print("a b c".split(), list("a b c"))

# Remove duplicates, preserving order
data = [3, 1, 3, 2, 1]
print(list(dict.fromkeys(data)))       # [3, 1, 2]
print(sorted(set(data)))               # [1, 2, 3] (sorted, order lost)

# ----------------------------------------------------------------------
section("6. ROUNDING vs TRUNCATING vs FLOORING")
# ----------------------------------------------------------------------
import math
x = -2.5
print(int(x), round(x), math.floor(x), math.ceil(x))   # -2 -2 -3 -2
print(int(2.5), round(2.5), round(3.5))                # 2 2 4

# ----------------------------------------------------------------------
section("7. SAFE CONVERSION PATTERN (EAFP)")
# ----------------------------------------------------------------------
def to_int(text, default=None):
    """Return int(text) or default if conversion fails."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(to_int("12"), to_int("x", 0), to_int(None, -1), to_int("3.5"))

def read_number(text):
    """Try int, then float, else None."""
    for caster in (int, float):
        try:
            return caster(text)
        except ValueError:
            continue
    return None

print(read_number("10"), read_number("10.5"), read_number("ten"))

# ----------------------------------------------------------------------
section("8. TRICKY PREDICT-THE-OUTPUT")
# ----------------------------------------------------------------------
print(bool("False"))        # ?
print(int(True) + int("2")) # ?
print(str(1) + str(2))      # ?
print(float("nan") == float("nan"))  # ?
print(list("123"))          # ?
print(sum(map(int, "12345")))  # ?
print(type(5 / 1), type(5 // 1), type(5.0 // 1))  # ?
