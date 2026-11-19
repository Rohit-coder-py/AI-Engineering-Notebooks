"""
================================================================================
DAY 1 — Type Conversion (Implicit vs Explicit)
================================================================================

INTERVIEW MINDSET: Python is strongly typed, so unrelated types don't coerce
silently. Know explicit constructors (int, float, str, bool, list, tuple, set)
and the truthiness rules that drive bool conversion.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. IMPLICIT (AUTOMATIC) CONVERSION — coercion
# ------------------------------------------------------------------------------
# Python implicitly converts between numeric types in mixed arithmetic.
# int + float -> float

a = 5          # int
b = 2.5        # float
c = a + b      # 7.5  (int coerced to float)
print(c, type(c))   # 7.5 <class 'float'>

# int / int always gives float in Python 3:
print(10 / 4)          # 2.5

# ------------------------------------------------------------------------------
# 2. EXPLICIT TYPE CONVERSION (constructors / casting)
# ------------------------------------------------------------------------------
# int(), float(), str(), bool(), list(), tuple(), set(), dict()

# int()
print(int(3.9))          # 3      (truncates toward zero — NOT rounding)
print(int(-3.9))         # -3
print(int("42"))         # 42
print(int("0b1010", 2))  # 10     (base given)
# print(int("3.5"))      # ValueError — can't parse float-string directly
# print(int("abc"))      # ValueError

# float()
print(float(5))          # 5.0
print(float("3.14"))     # 3.14
print(float("nan"))      # nan
print(float("inf"))      # inf

# str()
print(str(100))          # "100"
print(str([1, 2]))       # "[1, 2]"

# bool() — depends on TRUTHINESS (see next section)

# ------------------------------------------------------------------------------
# 3. TRUTHINESS / FALSY VALUES — what bool(x) returns
# ------------------------------------------------------------------------------
# Falsy: False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0), objects
#        with __bool__ returning False or __len__ returning 0
# Everything else is truthy.

tests = [False, None, 0, 0.0, "", [], (), {}, set(), range(0), 42, "hi", [1]]
for t in tests:
    print(f"{repr(t):<14} -> bool: {bool(t)}")

# Practical use: checking if a collection is empty
names = []
if not names:
    print("names is empty")

# ------------------------------------------------------------------------------
# 4. COMMON CONVERSION GOTCHAS (interview favorites)
# ------------------------------------------------------------------------------
# Gotcha 1: int("3.5") raises ValueError — convert via float first if needed.
print(int(float("3.5")))   # 3

# Gotcha 2: bool("False") is True — any non-empty string is truthy!
print(bool("False"))       # True   (don't use bool() to parse "true"/"false")

# Gotcha 3: round() uses banker's rounding (round half to even)
print(round(2.5))          # 2
print(round(3.5))          # 4

# Gotcha 4: float equality
print(0.1 + 0.2 == 0.3)    # False  (floating point representation)
print(abs((0.1 + 0.2) - 0.3) < 1e-9)   # True — compare with tolerance

# ------------------------------------------------------------------------------
# 5. CONVERSION BETWEEN COLLECTIONS
# ------------------------------------------------------------------------------
seq = [1, 2, 2, 3]
print(tuple(seq))          # (1, 2, 2, 3)
print(set(seq))            # {1, 2, 3}  (duplicates removed, order lost)
print(list("abc"))         # ['a', 'b', 'c']

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: int(3.9) — is it rounded or truncated?
# A: Truncated toward zero. int(3.9) == 3, int(-3.9) == -3. Use round() for rounding.
#
# Q: bool("False") — True or False?
# A: True. Non-empty strings are truthy regardless of content.
#
# Q: Why is 0.1 + 0.2 != 0.3?
# A: IEEE 754 binary floating point can't represent 0.1/0.2 exactly. Compare
#    floats with a tolerance (epsilon), never with ==.

if __name__ == "__main__":
    print("Run directly to see type conversion behavior.")
