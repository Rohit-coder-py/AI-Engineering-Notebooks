"""
================================================================================
DAY 2 — break, continue, pass
================================================================================

INTERVIEW MINDSET: Know exact control-flow behavior of each, where they're
legal (loops only for break/continue; pass anywhere), and common patterns
(search, skip invalid input, placeholder stubs).
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. break — exit the loop immediately
# ------------------------------------------------------------------------------
# The loop stops; the loop's else clause (if present) does NOT run.

for i in range(1, 11):
    if i == 5:
        break                 # exit loop entirely when i reaches 5
    print(i, end=" ")
print("\n--- loop ended ---")   # prints 1 2 3 4 then ends

# Practical: search-and-stop
target = 7
numbers = [2, 4, 6, 7, 8, 10]
for n in numbers:
    if n == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found")   # runs only if no break

# ------------------------------------------------------------------------------
# 2. continue — skip to the next iteration
# ------------------------------------------------------------------------------
# Current iteration ends immediately; loop proceeds with the next item.

print("Odd numbers 1-9:")
for i in range(1, 10):
    if i % 2 == 0:
        continue              # skip even numbers
    print(i, end=" ")
print()

# Practical: skip empty/invalid lines
lines = ["hello", "", "world", None, "python"]
for line in lines:
    if not line:              # skips "" and None
        continue
    print(f"Processing: {line}")

# ------------------------------------------------------------------------------
# 3. pass — do nothing (placeholder)
# ------------------------------------------------------------------------------
# A null statement. Syntactically required where Python expects a block but
# you don't want any logic yet. Commonly used for stubs / future implementation.

def future_feature():
    pass                      # TODO: implement later

class NotImplementedYet:
    pass

for i in range(5):
    if i % 2 == 0:
        pass                  # do nothing for even numbers
    else:
        print(i)              # 1 3

# ------------------------------------------------------------------------------
# 4. break vs continue vs pass — side-by-side
# ------------------------------------------------------------------------------
nums = [1, 2, 3, 4, 5]

print("break at 3:  ", end="")
for n in nums:
    if n == 3:
        break
    print(n, end=" ")
print()

print("continue 3:  ", end="")
for n in nums:
    if n == 3:
        continue
    print(n, end=" ")
print()

print("pass at 3:   ", end="")
for n in nums:
    if n == 3:
        pass
    print(n, end=" ")
print()

# ------------------------------------------------------------------------------
# 5. NESTED LOOPS + break (break only exits the INNERMOST loop)
# ------------------------------------------------------------------------------
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

found = False
for row in matrix:
    for val in row:
        if val == 5:
            print("Found 5!")
            found = True
            break            # exits the inner loop only
    if found:
        break                # exit the outer loop too

# Alternative clean approach: wrap in a function and return
def find_value(matrix, target):
    for row in matrix:
        for val in row:
            if val == target:
                return True
    return False

print(find_value(matrix, 5))   # True
print(find_value(matrix, 99))  # False

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Where can break/continue be used?
# A: Only inside loops (for/while). Using them elsewhere is a SyntaxError.
#
# Q: Where can pass be used?
# A: Anywhere a statement is expected (function bodies, classes, loops,
#    conditionals). It's a no-op placeholder.
#
# Q: Does break exit all nested loops?
# A: No. break exits only the innermost loop containing it. Use a flag,
#    function return, or labeled logic for outer loops.

if __name__ == "__main__":
    print("Run directly to see break/continue/pass in action.")
