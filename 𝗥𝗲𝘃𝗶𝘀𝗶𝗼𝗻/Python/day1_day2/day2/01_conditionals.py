"""
================================================================================
DAY 2 — Conditionals (if / elif / else, nested, ternary)
================================================================================

INTERVIEW MINDSET: Understand truthiness (what counts as False), the if-elif-else
chain short-circuits (only ONE branch runs), nested conditionals, and the
ternary operator. Avoid common indentation mistakes.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. BASIC if / elif / else
# ------------------------------------------------------------------------------
# Only the FIRST True condition's block runs; the rest are skipped (short-circuit).
# Python uses INDENTATION to define blocks — no braces {}.

score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"  # this runs (score >= 80 and score < 90)
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score {score} -> Grade {grade}")  # Score 85 -> Grade B

# ------------------------------------------------------------------------------
# 2. TRUTHINESS IN CONDITIONS
# ------------------------------------------------------------------------------
# The condition after 'if' is evaluated for truthiness, not compared to True.
# Falsy: False, None, 0, 0.0, "", [], (), {}, set(), range(0)
# Everything else: truthy

user = ""
if user:
    print("logged in")
else:
    print("no user")  # runs, because "" is falsy

items = [1, 2, 3]
if items:
    print("list not empty")  # runs

# Anti-pattern: don't compare to True/False explicitly
if is_active == True:  # bad style
    pass
if is_active:  # good style
    pass

# ------------------------------------------------------------------------------
# 3. NESTED CONDITIONALS
# ------------------------------------------------------------------------------
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Entry granted")
    else:
        print("ID required")
else:
    print("Underage")

# Can often be flattened with 'and':
if age >= 18 and has_id:
    print("Entry granted (flattened)")

# ------------------------------------------------------------------------------
# 4. TERNARY / CONDITIONAL EXPRESSION (value-returning if-else)
# ------------------------------------------------------------------------------
status = "adult" if age >= 18 else "minor"
print(status)  # adult

# Nested ternary (works, but hurts readability — avoid in production):
result = "A" if score >= 90 else ("B" if score >= 80 else "C")
print(result)

# ------------------------------------------------------------------------------
# 5. MATCH / CASE (STRUCTURAL PATTERN MATCHING — Python 3.10+)
# ------------------------------------------------------------------------------
# Worth knowing for interviews; it's like switch in other languages but more
# powerful (can match sequences, mappings, classes, with guards).

command = "save"

match command:
    case "save":
        print("Saving file...")
    case "load":
        print("Loading file...")
    case "exit":
        print("Exiting...")
    case _:  # default / wildcard
        print("Unknown command")

# With a guard:
status_code = 404
match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _ if 400 <= status_code < 500:
        print("Client error")
    case _ if 500 <= status_code < 600:
        print("Server error")
    case _:
        print("Other")

# ------------------------------------------------------------------------------
# 6. COMMON INTERVIEW PITFALLS
# ------------------------------------------------------------------------------
# a) Forgetting the colon (:) after if/elif/else -> SyntaxError
# b) Wrong indentation -> IndentationError or silent logic bugs
# c) Using 'is' to compare values instead of '=='
# d) Multiple if statements instead of elif -> every block can run, not just one
# e) Comparing to True explicitly: if x == True (use if x:)

# Example of (d) bug:
marks = 85
if marks >= 90:
    print("A")
if marks >= 80:  # this ALSO runs — not exclusive!
    print("B")  # prints both A... no, actually only B here, but logic wrong for grades

# Correct:
if marks >= 90:
    print("A")
elif marks >= 80:
    print("B")

if __name__ == "__main__":
    print("Run directly to see conditionals in action.")
