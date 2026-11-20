"""
================================================================================
DAY 1 — Interview Questions (Theory + Practical)
================================================================================

INSTRUCTION: Try answering each question yourself FIRST. Then read the answer
and run the code snippet under each practical section.
================================================================================
"""

# ==============================================================================
# THEORY QUESTIONS
# ==============================================================================

"""
Q1. Are Python variables statically or dynamically typed? Is Python strongly or
    weakly typed? Give examples.

A: Dynamically typed — a name's type is decided at runtime by the object it
   refers to; a name can be rebound to different types.
   Strongly typed — Python does NOT implicitly coerce unrelated types.
   Example: "5" + 2 raises TypeError (unlike JavaScript).

Q2. What is the difference between '==' and 'is'? When do you use each?

A: '==' checks value equality (__eq__). 'is' checks object identity (same id()).
   Use 'is' for singletons: `if x is None`. Never use 'is' to compare int/str
   values because of interning quirks.

Q3. What happens with a = b = [] then b.append(1)? Why?

A: Both names point to the SAME list object, so a becomes [1] too. This is
   aliasing. To get independent lists, use a = []; b = [] or .copy().

Q4. What is the output of bool([]), bool("0"), bool(False), bool(None)?

A: False, True, False, False. Empty collections and None are falsy; the
   string "0" is non-empty so truthy.

Q5. Is bool a subclass of int? What is the practical impact?

A: Yes. True == 1, False == 0. sum([True, True]) == 2. This is why bool
   works in arithmetic contexts.

Q6. Do Python ints overflow?

A: No. Python 3 ints have arbitrary precision, limited only by memory.
   2 ** 100000 works fine.

Q7. Are type hints enforced at runtime?

A: No. def f(n: int) -> int: ... hints are metadata for tools (mypy, IDEs).
   Runtime does not enforce them; use isinstance() if you need checks.

Q8. What is the difference between implicit and explicit type conversion?
    Give an example of each.

A: Implicit: 5 + 2.5 -> 7.5 (Python auto-coerces numeric types).
   Explicit: int("42"), float(5), str([1,2]) (programmer calls a constructor).

Q9. What does the walrus operator := do? Give a use case.

A: Assignment expression (Py 3.8+). Assigns inside an expression. Use case:
   avoiding a redundant len() call: if (n := len(items)) > 5: ...

Q10. What is duck typing? Give an example.

A: "If it walks like a duck and quacks like a duck, it's a duck." We check
   whether an object supports needed methods/attributes, not its type.
   Example: any object with a .read() method can be used like a file.
"""

# ==============================================================================
# PRACTICAL QUESTIONS (write code, then run)
# ==============================================================================

"""
P1. Write code that demonstrates a name being rebound to objects of three
    different types, printing type() each time.

P2. Swap two variables without a temporary variable.

P3. Create a list, assign it to a second variable, mutate via the second
    variable, and show that the first also changed. Then fix it with a copy.

P4. Show an example where '==' is True but 'is' is False.

P5. Convert the string "123.45" to an int (handle the ValueError path).

P6. Write a function that returns "Even" or "Odd" using a ternary expression.
"""

# --- P1 ---
name = 42
print("P1:", name, type(name))
name = 3.14
print("P1:", name, type(name))
name = "hello"
print("P1:", name, type(name))

# --- P2 ---
a, b = 10, 20
a, b = b, a
print("P2:", a, b)   # 20 10

# --- P3 ---
original = [1, 2, 3]
alias = original
alias.append(4)
print("P3 before fix:", original)   # [1, 2, 3, 4] — aliasing!

original = [1, 2, 3]
safe = original.copy()
safe.append(4)
print("P3 after fix :", original)   # [1, 2, 3] — independent

# --- P4 ---
x = [1, 2, 3]
y = [1, 2, 3]
print("P4:", x == y, x is y)   # True False

# --- P5 ---
s = "123.45"
try:
    print("P5:", int(s))
except ValueError:
    print("P5:", int(float(s)))   # 123

# --- P6 ---
def parity(n):
    return "Even" if n % 2 == 0 else "Odd"

print("P6:", parity(4), parity(7))

if __name__ == "__main__":
    print("Day 1 interview snippets ran above.")
