"""
DAY 2 | 05 - CONDITIONALS
========================
if, elif, else, nested conditionals, truthiness, ternary, match-case,
common patterns and pitfalls.

Run: python 05_conditionals.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. if / elif / else")
# ----------------------------------------------------------------------
# THEORY
# - Python uses INDENTATION (4 spaces) to define blocks, not braces.
# - Conditions are evaluated for TRUTHINESS (not just True/False).
# - elif chain stops at the FIRST true branch; order matters.
# - else is optional and runs only if nothing above matched.
marks = 78
if marks >= 90:
    grade = "A+"
elif marks >= 75:
    grade = "A"
elif marks >= 60:
    grade = "B"
else:
    grade = "C"
print(marks, "->", grade)

# Order bug example: broad condition first hides the narrow ones
score = 95
if score >= 50:
    print("(bug) always lands here even for 95")
elif score >= 90:
    print("never reached")

# ----------------------------------------------------------------------
section("2. TRUTHINESS in conditions")
# ----------------------------------------------------------------------
items = []
if items:                    # Pythonic: no need for len(items) > 0
    print("has items")
else:
    print("empty list")

name = ""
if not name:
    print("name is empty")

value = 0
if value is not None and value == 0:
    print("0 is a valid value, don't treat as missing")
# Trap:  if value:  would be False for 0 - choose 'is None' when 0 is meaningful.

# ----------------------------------------------------------------------
section("3. NESTED CONDITIONALS")
# ----------------------------------------------------------------------
age, has_id = 20, True
if age >= 18:
    if has_id:
        print("entry allowed")
    else:
        print("show ID")
else:
    print("underage")

# Flatten with logical operators / early returns (cleaner):
if age >= 18 and has_id:
    print("entry allowed (flat)")

def classify(n):
    """Guard clauses > deep nesting."""
    if not isinstance(n, (int, float)):
        return "not a number"
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"

print(classify(5), classify(-1), classify(0), classify("x"))

# ----------------------------------------------------------------------
section("4. COMPARISON TRICKS")
# ----------------------------------------------------------------------
x = 15
if 10 <= x <= 20:             # chained comparison
    print("in range")
if x in (10, 15, 20):         # membership instead of x==10 or x==15 or x==20
    print("in set of options")
if x % 3 == 0 and x % 5 == 0:
    print("FizzBuzz case")
# any / all
nums = [2, 4, 6]
print(all(n % 2 == 0 for n in nums), any(n > 5 for n in nums))

# ----------------------------------------------------------------------
section("5. TERNARY EXPRESSION")
# ----------------------------------------------------------------------
n = 7
print("even" if n % 2 == 0 else "odd")
absolute = n if n >= 0 else -n
print(absolute)

# ----------------------------------------------------------------------
section("6. match-case (structural pattern matching, Python 3.10+)")
# ----------------------------------------------------------------------
def http_status(code):
    match code:
        case 200:
            return "OK"
        case 301 | 302:
            return "Redirect"
        case 404:
            return "Not Found"
        case c if 500 <= c < 600:
            return "Server Error"
        case _:
            return "Unknown"

print([http_status(c) for c in (200, 302, 404, 503, 999)])

def describe(point):
    match point:
        case (0, 0):
            return "origin"
        case (x, 0):
            return f"on x-axis at {x}"
        case (0, y):
            return f"on y-axis at {y}"
        case (x, y):
            return f"point {x},{y}"

print(describe((0, 0)), describe((5, 0)), describe((3, 4)))

# ----------------------------------------------------------------------
section("7. CLASSIC PROBLEMS")
# ----------------------------------------------------------------------
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print([is_leap(y) for y in (1900, 2000, 2024, 2023)])

def largest_of_three(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    return c

print(largest_of_three(3, 9, 4))

def bmi_category(w_kg, h_m):
    bmi = w_kg / (h_m ** 2)
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"

print(bmi_category(70, 1.75))

# ----------------------------------------------------------------------
section("8. PITFALLS")
# ----------------------------------------------------------------------
# 1. = vs ==          if x = 5:  -> SyntaxError
# 2. is vs ==         if x is 5: -> works by accident (SyntaxWarning)
# 3. "or" misuse:     if x == 1 or 2:  -> always True (2 is truthy)
x = 5
print("buggy or:", bool(x == 1 or 2))
print("correct :", x in (1, 2))
# 4. Comparing floats with ==  -> use math.isclose
# 5. Forgetting colon / inconsistent indentation -> SyntaxError / IndentationError
# 6. Mutable default / None check: use 'is None', not '== None'
