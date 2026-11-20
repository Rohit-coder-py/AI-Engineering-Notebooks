"""
================================================================================
DAY 1 — Python Operators (with precedence and internship gotchas)
================================================================================

INTERVIEW MINDSET: Know precedence order, short-circuit evaluation, chained
comparisons, the walrus operator, identity/membership operators, and truthiness.
================================================================================
"""

# ------------------------------------------------------------------------------
# 0. OPERATOR PRECEDENCE (high to low) — the order Python evaluates expressions
# ------------------------------------------------------------------------------
# 1. ()                      parentheses
# 2. x[index], x.attr, f()   subscription, attribute, call
# 3. await                   (async)
# 4. **                      exponentiation (right-associative)
# 5. +x -x ~x                unary plus/minus, bitwise NOT
# 6. * @ / // %              multiplication, division, floor division, modulo
# 7. + -                     addition, subtraction
# 8. << >>                   shifts
# 9. &                       bitwise AND
# 10. ^                      bitwise XOR
# 11. |                      bitwise OR
# 12. in not in is is not < <= > >= != ==   comparisons, membership, identity
# 13. not                    logical NOT
# 14. and                    logical AND
# 15. or                     logical OR
# 16. if – else              conditional expression (ternary)
# 17. lambda                 lambda
# 18. = += -= ...            assignment (including walrus :=)

print(2 + 3 * 4)             # 14   (* before +)
print((2 + 3) * 4)           # 20   (parentheses first)
print(2 ** 3 ** 2)           # 512  (** is right-associative: 2 ** (3 ** 2))

# ------------------------------------------------------------------------------
# 1. ARITHMETIC OPERATORS
# ------------------------------------------------------------------------------
print(7 + 3)                 # 10
print(7 - 3)                 # 4
print(7 * 3)                 # 21
print(7 / 3)                 # 2.333... (true division -> float)
print(7 // 3)                # 2    (floor division)
print(7 % 3)                 # 1    (modulo / remainder)
print(2 ** 5)                # 32   (exponentiation)

# Floor division with negatives rounds toward negative infinity:
print(-7 // 3)               # -3   (not -2!)
print(-7 % 3)                # 2

# ------------------------------------------------------------------------------
# 2. COMPARISON OPERATORS
# ------------------------------------------------------------------------------
print(5 == 5)                # True
print(5 != 3)                # True
print(5 > 3)                 # True
print(3 < 5)                 # True
print(5 >= 5)                # True
print(3 <= 5)                # True

# Chained comparisons — Pythonic and interview-worthy:
age = 25
print(18 <= age < 65)        # True   (means: 18 <= age and age < 65)
# Note: this does NOT short-circuit like C; each comparison evaluated as needed.

# ------------------------------------------------------------------------------
# 3. ASSIGNMENT OPERATORS
# ------------------------------------------------------------------------------
x = 10
x += 5                       # x = x + 5
x -= 3
x *= 2
x /= 4
x //= 3
x %= 2
x **= 2
print(x)

# Walrus operator := (Python 3.8+) — assign inside an expression
# Useful in while loops and comprehensions to avoid calling twice.
if (n := len("hello")) > 3:
    print(f"Length is {n}")   # Length is 5

# ------------------------------------------------------------------------------
# 4. LOGICAL OPERATORS — short-circuit evaluation
# ------------------------------------------------------------------------------
# and: returns the first falsy operand, else the last operand.
# or:  returns the first truthy operand, else the last operand.
# not: returns a bool.

print(True and "hello")      # 'hello'   (first truthy? no—returns last if all true)
print(False and "hello")     # False
print("" or "default")       # 'default' ('' is falsy, so returns 'default')
print([1, 2] or [3])         # [1, 2]    (truthy, returns first)
print(not True)              # False

# Short-circuit: the second operand may never be evaluated.
def side_effect():
    print("side_effect ran")
    return True

print(False and side_effect())   # 'side_effect' NOT printed
print(True or side_effect())     # 'side_effect' NOT printed

# Common idiom: default values
username = "" or "guest"
print(username)             # 'guest'

# ------------------------------------------------------------------------------
# 5. IDENTITY OPERATORS
# ------------------------------------------------------------------------------
# is / is not — compare object identity (id), not values.
print(None is None)             # True
print([] is [])                 # False
a = [1, 2]
b = a
print(a is b)                   # True

# ------------------------------------------------------------------------------
# 6. MEMBERSHIP OPERATORS
# ------------------------------------------------------------------------------
# in / not in — check if a value exists in a container (list, str, tuple, set, dict)
print(2 in [1, 2, 3])           # True
print("a" in "apple")           # True
print(5 not in [1, 2, 3])       # True
d = {"a": 1}
print("a" in d)                 # True   (checks KEYS in a dict — O(1))

# ------------------------------------------------------------------------------
# 7. BITWISE OPERATORS
# ------------------------------------------------------------------------------
print(5 & 3)                    # 1   (101 & 011 = 001)
print(5 | 3)                    # 7   (101 | 011 = 111)
print(5 ^ 3)                    # 6   (101 ^ 011 = 110)
print(~5)                       # -6  (two's complement)
print(5 << 1)                   # 10  (shift left)
print(5 >> 1)                   # 2   (shift right)

# ------------------------------------------------------------------------------
# 8. TERNARY / CONDITIONAL EXPRESSION
# ------------------------------------------------------------------------------
status = "adult" if age >= 18 else "minor"
print(status)                   # adult

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: What is short-circuit evaluation?
# A: 'and' stops at the first falsy value; 'or' stops at the first truthy value.
#    Remaining operands are NOT evaluated (important for side effects).
#
# Q: What does x and y return if both are truthy?
# A: y (the last operand). Logical operators return operands, not just bools.
#
# Q: Difference between /= and //= ?
# A: /= true division (float). //= floor division (int, rounds toward -inf).
#
# Q: When to use 'is' instead of '=='?
# A: Only for identity checks — primarily `x is None` / `x is not None`.
#    Never use `is` to compare int/str values.

if __name__ == "__main__":
    print("Run directly to see operator examples.")
