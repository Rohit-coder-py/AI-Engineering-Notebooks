"""
DAY 1 | 04 - OPERATORS
=====================
Arithmetic, comparison, logical, bitwise, assignment, identity, membership,
precedence, ternary, walrus.

Run: python 04_operators.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. ARITHMETIC  + - * / // % **")
# ----------------------------------------------------------------------
a, b = 17, 5
print(a + b, a - b, a * b)
print(a / b)      # true division -> always float
print(a // b)     # floor division
print(a % b)      # modulus
print(a ** b)     # power
# Negative numbers: // floors toward -infinity, % has sign of the divisor
print(-7 // 2, -7 % 2, 7 // -2, 7 % -2)    # -4 1 -4 -1
print(divmod(-7, 2))                       # (-4, 1)  invariant: a == (a//b)*b + a%b
print(2 ** -1, 2 ** 0.5, -2 ** 2, (-2) ** 2)  # 0.5 1.414.. -4 4  (** binds tighter than unary -)
print(10 % 3 == 1, 10 % 2 == 0)           # odd/even checks
print("ab" * 3, [0] * 3, "a" + "b")         # operator overloading

# ----------------------------------------------------------------------
section("2. COMPARISON  == != < > <= >=")
# ----------------------------------------------------------------------
print(5 == 5.0, "a" < "b", [1, 2] < [1, 3], (1, 2) == (1, 2))
print(1 < 5 < 10)           # chained: 1<5 and 5<10
print(1 < 5 > 3 < 4)        # True
print("apple" < "Apple")     # False: lowercase letters have larger code points
# Don't chain confusingly: print(1 == 1 in [1])  -> (1==1) and (1 in [1])

# ----------------------------------------------------------------------
section("3. LOGICAL  and or not  (short-circuit, return operands!)")
# ----------------------------------------------------------------------
print(True and False, True or False, not True)
# 'and' returns first FALSY operand, else the last operand
print(5 and 10, 0 and 10, "" and "x")        # 10 0 ''
# 'or' returns first TRUTHY operand, else the last operand
print(5 or 10, 0 or 10, "" or "default")     # 5 10 default
# Idiom: default values
user_name = ""
print(user_name or "Guest")
# Short-circuit prevents errors:
x = 0
print(x != 0 and 10 / x > 1)   # False, no ZeroDivisionError
# Precedence: not > and > or
print(True or False and False)  # True  (and first)

# ----------------------------------------------------------------------
section("4. BITWISE  & | ^ ~ << >>")
# ----------------------------------------------------------------------
x, y = 0b1100, 0b1010   # 12, 10
print(f"{x & y:04b} {x | y:04b} {x ^ y:04b}")   # 1000 1110 0110
print(~5, 5 << 1, 5 >> 1, 1 << 4)              # -6 10 2 16
print("is power of 2 (16):", 16 & (16 - 1) == 0)
print("is odd (7):", bool(7 & 1))
# swap using XOR
p, q = 3, 9
p ^= q; q ^= p; p ^= q
print(p, q)

# ----------------------------------------------------------------------
section("5. ASSIGNMENT  = += -= *= /= //= %= **= &= |= ^= <<= >>=")
# ----------------------------------------------------------------------
n = 10
n += 2; n -= 1; n *= 3; n //= 2; n **= 2; n %= 7
print(n)
lst = [1]
lst += [2, 3]        # in-place extend
lst *= 2
print(lst)

# ----------------------------------------------------------------------
section("6. IDENTITY  is, is not   |   MEMBERSHIP  in, not in")
# ----------------------------------------------------------------------
a = [1, 2]; b = [1, 2]; c = a
print(a == b, a is b, a is c, a is not b)
print(3 in [1, 2, 3], "a" in "apple", "x" not in "apple", 1 in {1: "v"})  # dict -> keys
print("ell" in "hello")   # substring test for str

# ----------------------------------------------------------------------
section("7. TERNARY (conditional expression)")
# ----------------------------------------------------------------------
age = 20
status = "adult" if age >= 18 else "minor"
print(status)
print("even" if 7 % 2 == 0 else "odd")
# nested (use sparingly)
marks = 72
print("A" if marks >= 90 else "B" if marks >= 70 else "C")

# ----------------------------------------------------------------------
section("8. WALRUS  :=  (assignment expression, 3.8+)")
# ----------------------------------------------------------------------
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"list is long ({n} items)")
# useful in while loops:
# while (line := input()) != "quit": ...

# ----------------------------------------------------------------------
section("9. PRECEDENCE (high -> low)")
# ----------------------------------------------------------------------
# ()  **  +x -x ~x  * / // %  + -  << >>  &  ^  |  comparisons/in/is
# not  and  or  ternary  :=
print(2 + 3 * 4 ** 2 / 8)       # 8.0
print(not 1 + 1 == 2)           # not ((1+1)==2) -> False
print(2 ** 3 ** 2)              # right-associative -> 2**9 = 512
print(100 / 10 / 5)             # left-associative -> 2.0
# When in doubt, use parentheses. Readability > cleverness.

# ----------------------------------------------------------------------
section("10. PREDICT THE OUTPUT")
# ----------------------------------------------------------------------
print(10 // 3 * 3 + 10 % 3)             # ?
print(not None and 1 or 2)              # ?
print(3 > 2 > 1, 3 > 2 < 1)             # ?
print("a" * 0 or "empty")               # ?
print(bool(0 or [] or "x"))             # ?
print(5 & 3, 5 | 3, 5 ^ 3)              # ?
print(-3 ** 2)                          # ?
print(0.1 * 3 == 0.3)                   # ?
