"""
================================================================================
DAY 1 — Multiple Variable Assignment (Tuple Unpacking)
================================================================================

INTERVIEW MINDSET: Know chain assignment pitfalls with mutables, parallel
assignment for swapping, and extended unpacking with the * operator.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. CHAIN ASSIGNMENT: a = b = c = value
# ------------------------------------------------------------------------------
# All names bind to the SAME object. Fine for immutables, DANGEROUS for mutables.

a = b = c = 10
print(a, b, c)              # 10 10 10

# DANGER with mutable objects:
list_a = list_b = [1, 2, 3]
list_a.append(4)
print(list_a)               # [1, 2, 3, 4]
print(list_b)               # [1, 2, 3, 4]  <- SAME object mutated! Surprise!

# Correct way to create independent copies:
list_a = [1, 2, 3]
list_b = list(list_a)       # or list_a.copy() / list_a[:]
list_a.append(4)
print(list_a)               # [1, 2, 3, 4]
print(list_b)               # [1, 2, 3]

# ------------------------------------------------------------------------------
# 2. PARALLEL (TUPLE) ASSIGNMENT: a, b, c = 1, 2, 3
# ------------------------------------------------------------------------------
# The RHS is a tuple; Python unpacks it into the names on the LHS.
# The number of names must match the number of values.

a, b, c = 1, 2, 3
print(a, b, c)              # 1 2 3

# Works with any iterable of the right size:
x, y = [10, 20]
p, q = (1, 2)
m, n = "ab"
print(x, y, p, q, m, n)     # 10 20 1 2 a b

# ------------------------------------------------------------------------------
# 3. SWAPPING VARIABLES (the Pythonic way)
# ------------------------------------------------------------------------------
# No temp variable needed. The RHS tuple is built first, then unpacked.

a, b = 10, 20
a, b = b, a
print(a, b)                 # 20 10

# ------------------------------------------------------------------------------
# 4. EXTENDED UNPACKING WITH *
# ------------------------------------------------------------------------------
# *rest collects remaining items into a list. Only ONE starred target allowed.

head, *middle, tail = [1, 2, 3, 4, 5]
print(head)     # 1
print(middle)   # [2, 3, 4]
print(tail)     # 5

first, *rest = [1, 2, 3]
print(first)    # 1
print(rest)     # [2, 3]

*leading, last = [1, 2, 3]
print(leading)  # [1, 2]
print(last)     # 3

# ------------------------------------------------------------------------------
# 5. UNPACKING IN FUNCTION CALLS AND RETURNING MULTIPLE VALUES
# ------------------------------------------------------------------------------
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

# A function "returns multiple values" — actually it returns ONE tuple,
# which we unpack.
minimum, maximum, average = get_stats([10, 20, 30, 40])
print(minimum, maximum, average)   # 10 40 25.0

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: What does a, b = b, a do under the hood?
# A: Python builds a temporary tuple (b, a) on the RHS, then unpacks it into
#    a and b. No explicit temp variable needed in your source code.
#
# Q: Is a = b = [] safe?
# A: No. Both names point to the SAME list object. Mutating one mutates both.
#    Use separate literals or .copy() when you need independence.
#
# Q: Can you unpack more values than variables?
# A: Only with *rest to collect the surplus; otherwise ValueError:
#    too many values to unpack (or not enough values to unpack).

if __name__ == "__main__":
    print("Run directly to see multiple assignment examples.")
