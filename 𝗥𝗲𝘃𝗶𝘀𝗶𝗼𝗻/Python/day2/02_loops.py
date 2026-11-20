"""
================================================================================
DAY 2 — Loops (for / while, range, enumerate, zip, loop else)
================================================================================

INTERVIEW MINDSET: Know when to use for vs while, loop-else semantics,
enumerate/zip for clean iteration, and that looping directly over containers
is more Pythonic than indexing with range(len(...)).
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. for LOOP — iterate over any iterable (list, str, tuple, set, dict, range)
# ------------------------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:           # preferred Pythonic style
    print(fruit)

# Avoid C-style indexing unless you actually need the index:
# for i in range(len(fruits)):   # less Pythonic
#     print(fruits[i])

# Strings are iterable too:
for ch in "Python":
    print(ch, end=" ")
print()

# ------------------------------------------------------------------------------
# 2. range() — generate integer sequences
# ------------------------------------------------------------------------------
# range(start, stop, step) — stop is EXCLUSIVE
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(2, 7)))       # [2, 3, 4, 5, 6]
print(list(range(1, 10, 2)))   # [1, 3, 5, 7, 9]

# Classic idiom: repeat N times
for _ in range(5):             # _ = throwaway variable
    print("hello", end=" ")
print()

# ------------------------------------------------------------------------------
# 3. enumerate() — index + value together
# ------------------------------------------------------------------------------
for index, fruit in enumerate(fruits):
    print(index, fruit)

# Custom start index:
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

# ------------------------------------------------------------------------------
# 4. zip() — iterate multiple iterables in parallel
# ------------------------------------------------------------------------------
names = ["rohit", "amit", "sara"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# zip stops at the SHORTEST iterable:
for a, b in zip([1, 2, 3], ["a", "b"]):
    print(a, b)   # only 2 pairs

# zip_longest from itertools when you want to keep going:
from itertools import zip_longest
for a, b in zip_longest([1, 2], ["a", "b", "c"], fillvalue=None):
    print(a, b)

# ------------------------------------------------------------------------------
# 5. while LOOP — repeat while condition is truthy
# ------------------------------------------------------------------------------
count = 0
while count < 3:
    print("count is", count)
    count += 1

# Infinite loop with break (must have an exit condition!):
# while True:
#     ...
#     break

# ------------------------------------------------------------------------------
# 6. LOOP else CLAUSE — Python-specific, often misunderstood
# ------------------------------------------------------------------------------
# The 'else' block runs when the loop FINISHES NATURALLY (not broken by 'break').
# Useful for search patterns: "did we find it?"

def contains_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            print("Found even:", n)
            break
    else:
        print("No even number found")

contains_even([1, 3, 5])       # No even number found
contains_even([1, 4, 5])       # Found even: 4

# while-else equivalent:
i = 0
while i < 3:
    print(i)
    i += 1
else:
    print("loop finished without break")

# ------------------------------------------------------------------------------
# 7. DICT ITERATION — keys by default; .items() for key-value
# ------------------------------------------------------------------------------
contact = {"name": "rohit", "city": "pune", "phone": "9999"}

for key in contact:            # iterates keys
    print(key)

for key, value in contact.items():
    print(f"{key}: {value}")

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: for vs while?
# A: for — when iterating over a known collection/iterable. while — when
#    repeating based on a condition (e.g., input validation, retry logic).
#
# Q: What does for-else do?
# A: else runs only if the loop was NOT terminated by break. Commonly used
#    in search algorithms.
#
# Q: range(len(x)) vs enumerate(x)?
# A: enumerate is preferred — cleaner, less error-prone, gives index+value.
#
# Q: Does zip stop at the shortest or longest iterable?
# A: Shortest. Use itertools.zip_longest to go to the longest.

if __name__ == "__main__":
    print("Run directly to see loops in action.")
