"""
DAY 1 | 02 - DATA TYPES
=======================
Covers: int, float, complex, bool, str, None, and a map of built-in containers.
Key ideas: mutable vs immutable, hashable, truthy/falsy, float precision.

Run: python 02_data_types.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. BIG PICTURE - BUILT-IN TYPES")
# ----------------------------------------------------------------------
# Numeric   : int, float, complex, bool (bool is a subclass of int)
# Text      : str
# Binary    : bytes, bytearray
# Sequence  : list, tuple, range, str
# Set types : set, frozenset
# Mapping   : dict
# Nothing   : NoneType (the single value None)
#
# MUTABLE   (can change in place): list, dict, set, bytearray
# IMMUTABLE (cannot change)      : int, float, complex, bool, str, tuple,
#                                  frozenset, bytes, None
samples = [10, 3.5, 2 + 3j, True, "hi", None, [1], (1,), {1}, {"a": 1}, b"x", range(3)]
for item in samples:
    print(f"{item!r:12} -> {type(item).__name__}")

# ----------------------------------------------------------------------
section("2. int")
# ----------------------------------------------------------------------
# - Arbitrary precision: no overflow, limited only by memory.
big = 2 ** 200
print(big)
print("digits:", len(str(big)))
print(1_000_000)              # underscores for readability
print(0b1010, 0o17, 0xFF)     # binary, octal, hex literals

# ----------------------------------------------------------------------
section("3. float (IEEE 754 double precision)")
# ----------------------------------------------------------------------
print(0.1 + 0.2)                      # 0.30000000000000004  (binary fraction issue)
print(0.1 + 0.2 == 0.3)               # False
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True  -> use this to compare floats
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))  # 0.3 exact; use for money
print(round(2.5), round(3.5), round(2.675, 2))  # banker's rounding! 2 4 2.67
print(float("inf") > 10**308, float("nan") == float("nan"))  # True False
print(7 / 2, 7 // 2, type(4 / 2))     # / always float

# ----------------------------------------------------------------------
section("4. complex")
# ----------------------------------------------------------------------
z = 3 + 4j
print(z.real, z.imag, abs(z), z.conjugate())

# ----------------------------------------------------------------------
section("5. bool - subclass of int")
# ----------------------------------------------------------------------
print(isinstance(True, int))     # True
print(True + True, True * 10)    # 2 10
print(sum([True, False, True]))  # 2  -> counting trick
# Truthy / Falsy values:
falsy = [0, 0.0, 0j, "", [], (), {}, set(), None, False, range(0)]
print("all falsy:", not any(falsy))
print(bool("False"), bool(" "), bool([0]))  # True True True (non-empty)

# ----------------------------------------------------------------------
section("6. str (immutable sequence of Unicode characters)")
# ----------------------------------------------------------------------
s = "Python Interview"
print(s[0], s[-1], s[0:6], s[::-1], s[::2])
# s[0] = "J"  -> TypeError: str is immutable
print(s.upper(), s.lower(), s.title(), s.swapcase())
print(s.find("Inter"), s.index("I"), s.count("e"), s.replace("Python", "Java"))
print("a,b,c".split(","), "-".join(["x", "y", "z"]), "  pad ".strip())
print(s.startswith("Py"), s.endswith("view"), "ntervi" in s)
print("abc".isalpha(), "123".isdigit(), "ab1".isalnum(), "  ".isspace())

name, score = "Harsh", 92.456
print("%s scored %.1f" % (name, score))            # old style
print("{} scored {:.1f}".format(name, score))      # str.format
print(f"{name} scored {score:.1f} | {score=:.2f}") # f-string (best)
print(f"{1234567:,} | {0.256:.1%} | {5:03d} | {'hi':>6} | {'hi':^6}|")
print(r"raw \n string", "multi\nline", """triple
quoted""")
print(len("héllo"), "héllo".encode("utf-8"))        # chars vs bytes

# ----------------------------------------------------------------------
section("7. None - the 'no value' singleton")
# ----------------------------------------------------------------------
result = None
print(result is None, result == None, bool(None))  # use 'is None'
def no_return():
    pass
print("function without return gives:", no_return())

# ----------------------------------------------------------------------
section("8. type(), isinstance(), id()")
# ----------------------------------------------------------------------
print(type(5) == int)               # works, but...
print(isinstance(5, int))           # preferred: respects inheritance
print(isinstance(True, int))        # True because bool subclasses int
print(type(True) == int)            # False (exact type check)
print(isinstance(5, (int, float)))  # check multiple types

# ----------------------------------------------------------------------
section("9. MUTABLE vs IMMUTABLE - the interview favourite")
# ----------------------------------------------------------------------
imm = (1, 2, [3, 4])
imm[2].append(5)     # allowed! the tuple still holds the SAME list object
print(imm)
# imm[0] = 9         # TypeError
print("hashable int:", hash(10))
print("hashable str:", hash("a") is not None)
try:
    hash([1, 2])
except TypeError as e:
    print("list unhashable ->", e)

# ----------------------------------------------------------------------
section("10. input() always returns str")
# ----------------------------------------------------------------------
# age = input("Age: ")      # "20" is a string!
# age = int(input("Age: "))  # convert before arithmetic
print("Remember: input() -> str. Convert explicitly.")
