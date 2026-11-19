"""
DAY 2 | 06 - LOOPS
==================
for, while, range, enumerate, zip, break, continue, pass, loop-else,
nested loops, comprehensions, common pitfalls.

Run: python 06_loops.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. for loop - iterates over any ITERABLE")
# ----------------------------------------------------------------------
# THEORY
# for x in iterable: -> calls iter(iterable), then next() until StopIteration.
# Python's for is a "for-each". No manual index needed.
for ch in "abc":
    print(ch, end=" ")
print()
for key in {"a": 1, "b": 2}:           # dict -> keys
    print(key, end=" ")
print()

# range(stop) / range(start, stop) / range(start, stop, step)
print(list(range(5)), list(range(2, 8)), list(range(10, 0, -3)))
# range is lazy (O(1) memory) and supports len(), indexing, 'in'
r = range(0, 1_000_000_000)
print(len(r), 999 in r, r[5])

# ----------------------------------------------------------------------
section("2. enumerate, zip, reversed, sorted")
# ----------------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]
for i, f in enumerate(fruits, start=1):   # index + value (don't use range(len()))
    print(i, f)

names = ["A", "B", "C"]
marks = [90, 80]
for n, m in zip(names, marks):            # stops at the SHORTEST
    print(n, m)
from itertools import zip_longest
print(list(zip_longest(names, marks, fillvalue=0)))

for f in reversed(fruits):
    print(f, end=" ")
print()
for f in sorted(fruits, key=len, reverse=True):
    print(f, end=" ")
print()

# ----------------------------------------------------------------------
section("3. while loop")
# ----------------------------------------------------------------------
# Use while when the NUMBER of iterations is unknown in advance.
n = 5
while n > 0:
    print(n, end=" ")
    n -= 1           # forgetting this = infinite loop
print("liftoff")

# Classic: digit sum / reverse a number
num, total, rev = 12345, 0, 0
while num > 0:
    digit = num % 10
    total += digit
    rev = rev * 10 + digit
    num //= 10
print("digit sum:", total, "| reversed:", rev)

# while True + break (menu / input validation pattern)
attempts = [0, 7, 3]    # simulate user input
idx = 0
while True:
    value = attempts[idx]; idx += 1
    if value >= 5:
        print("accepted", value)
        break
    print("rejected", value)

# ----------------------------------------------------------------------
section("4. break, continue, pass")
# ----------------------------------------------------------------------
for i in range(10):
    if i == 3:
        continue         # skip rest of THIS iteration
    if i == 6:
        break            # exit the loop completely
    print(i, end=" ")
print()

def todo_feature():
    pass                 # placeholder: does nothing, keeps syntax valid

class Empty:
    pass

for i in range(3):
    if i == 1:
        pass             # unlike continue, code below still runs
    print("pass-demo", i)

# ----------------------------------------------------------------------
section("5. loop-else (for/while ... else)")
# ----------------------------------------------------------------------
# else runs ONLY IF the loop ended normally (no break).
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break
    else:
        return True      # no divisor found
    return False

print([n for n in range(20) if is_prime(n)])

for x in [1, 2, 3]:
    if x == 5:
        break
else:
    print("5 not found (else ran because there was no break)")

# ----------------------------------------------------------------------
section("6. NESTED LOOPS & PATTERNS")
# ----------------------------------------------------------------------
for i in range(1, 5):
    print("*" * i)
for i in range(1, 4):
    print(" " * (3 - i) + "*" * (2 * i - 1))
for i in range(1, 4):
    print(*[i * j for j in range(1, 4)])    # multiplication table rows

# break only exits the INNERMOST loop. Use a flag/function to exit both:
def find_pair(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (nums[i], nums[j])    # return exits both loops
    return None
print(find_pair([2, 7, 11, 15], 9))

# ----------------------------------------------------------------------
section("7. COMPREHENSIONS (loop in one line)")
# ----------------------------------------------------------------------
squares = [x * x for x in range(6)]
evens = [x for x in range(10) if x % 2 == 0]
pairs = [(a, b) for a in range(2) for b in range(2)]
print(squares, evens, pairs)
print({x: x ** 2 for x in range(4)})       # dict comp
print({x % 3 for x in range(10)})          # set comp
total = sum(x * x for x in range(1000))    # generator expr: no list in memory
print(total)

# ----------------------------------------------------------------------
section("8. PITFALLS")
# ----------------------------------------------------------------------
# a) Modifying a list while iterating over it
nums = [1, 2, 3, 4, 5, 6]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)       # skips elements!
print("buggy :", nums)
nums = [1, 2, 3, 4, 5, 6]
nums = [n for n in nums if n % 2 != 0]
print("fixed :", nums)

# b) Loop variable leaks after the loop
for i in range(3):
    pass
print("i after loop:", i)    # 2

# c) range(len(x)) is usually a smell -> enumerate / direct iteration
# d) Infinite loop: while True without break, or condition never changes
# e) Late binding in closures inside loops
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])            # [2, 2, 2] not [0,1,2]
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])            # [0, 1, 2]

# ----------------------------------------------------------------------
section("9. CLASSIC PROBLEMS")
# ----------------------------------------------------------------------
def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0: out.append("FizzBuzz")
        elif i % 3 == 0: out.append("Fizz")
        elif i % 5 == 0: out.append("Buzz")
        else: out.append(str(i))
    return out
print(fizzbuzz(15))

def fib(n):
    a, b, out = 0, 1, []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out
print(fib(10))

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
print(factorial(5), factorial(0))

def is_palindrome(s):
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    return s == s[::-1]
print(is_palindrome("A man, a plan, a canal: Panama"))
