"""
================================================================================
DAY 2 — Lists (mutable ordered sequences)
================================================================================

INTERVIEW MINDSET: Lists are dynamic arrays. Know indexing/slicing, common
methods and their time complexity, list comprehensions, aliasing vs copying,
and that .sort() mutates in place while sorted() returns a new list.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. CREATION & INDEXING
# ------------------------------------------------------------------------------
nums = [10, 20, 30, 40, 50]

print(nums[0])    # 10  (first)
print(nums[-1])   # 50  (last)
print(nums[1:4])  # [20, 30, 40]  (slice: start inclusive, end exclusive)
print(nums[::-1]) # [50, 40, 30, 20, 10]  (reverse via slicing — new list)

# ------------------------------------------------------------------------------
# 2. CORE METHODS (mutating vs non-mutating)
# ------------------------------------------------------------------------------
nums = [10, 20, 30]

nums.append(40)           # add to end (O(1) amortized)
print(nums)               # [10, 20, 30, 40]

nums.insert(1, 15)        # insert at index (O(n) — shifts elements)
print(nums)               # [10, 15, 20, 30, 40]

nums.extend([50, 60])     # add multiple (O(k))
print(nums)               # [10, 15, 20, 30, 40, 50, 60]

nums.remove(20)           # remove first matching VALUE (O(n))
print(nums)               # [10, 15, 30, 40, 50, 60]

popped = nums.pop()       # remove & return last item (O(1))
print("popped:", popped)  # 60

popped_idx = nums.pop(0)  # remove & return item at index (O(n))
print("popped_idx:", popped_idx)  # 10

nums.clear()              # empty the list
print(nums)               # []

# ------------------------------------------------------------------------------
# 3. SEARCHING & ORDERING
# ------------------------------------------------------------------------------
data = [5, 2, 8, 1, 9]

print(8 in data)          # True  (membership — O(n))
print(data.index(8))      # 2     (index of first 8 — O(n); ValueError if missing)
print(data.count(2))      # 1     (occurrences)

data.sort()               # IN-PERMUTATION sort, returns None (O(n log n))
print(data)               # [1, 2, 5, 8, 9]

data.sort(reverse=True)
print(data)               # [9, 8, 5, 2, 1]

# sorted() returns a NEW list; original unchanged (works on any iterable)
original = [3, 1, 2]
sorted_new = sorted(original)
print(original)           # [3, 1, 2]  (unchanged)
print(sorted_new)         # [1, 2, 3]

# sort with key
words = ["banana", "apple", "cherry"]
words.sort(key=len)
print(words)              # ['apple', 'banana', 'cherry'] (by length)

# reverse in place
data = [1, 2, 3]
data.reverse()
print(data)               # [3, 2, 1]

# ------------------------------------------------------------------------------
# 4. LIST COMPREHENSIONS (interview favorite — concise + fast)
# ------------------------------------------------------------------------------
# [expression for item in iterable if condition]

squares = [x**2 for x in range(1, 6)]
print(squares)            # [1, 4, 9, 16, 25]

evens = [x for x in range(1, 11) if x % 2 == 0]
print(evens)              # [2, 4, 6, 8, 10]

# Nested comprehension (flatten a matrix):
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)               # [1, 2, 3, 4, 5, 6]

# Dict/set comprehensions preview (details in their files):
# {x: x**2 for x in range(5)}   -> {0: 0, 1: 1, 2: 4, ...}
# {x**2 for x in range(5)}      -> {0, 1, 4, 9, 16}

# ------------------------------------------------------------------------------
# 5. COPYING: SHALLOW vs ALIASING (critical)
# ------------------------------------------------------------------------------
a = [1, 2, [3, 4]]

b = a                      # aliasing — same object
b.append(5)
print(a)                   # [1, 2, [3, 4], 5] — a changed too!

b = a.copy()               # shallow copy (also list(a) / a[:] / a.__copy__())
b.append(5)
print(a)                   # [1, 2, [3, 4], 5] — wait, still changed?

# SHALLOW copy means nested objects are still shared:
b[2].append(99)
print(a)                   # [1, 2, [3, 4, 99], 5] — nested list shared!

# For full independence:
import copy
c = copy.deepcopy(a)
c[2].append(77)
print(a)                   # [1, 2, [3, 4, 99], 5] — truly independent now

# ------------------------------------------------------------------------------
# 6. TIME COMPLEXITY CHEAT SHEET
# ------------------------------------------------------------------------------
#   Indexing nums[i]              : O(1)
#   Append / pop from end         : O(1) amortized
#   Insert / pop from middle/start: O(n)  (elements shift)
#   remove(value) / index(value)  : O(n)  (scan)
#   in (membership)               : O(n)
#   sort                          : O(n log n)

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: .sort() vs sorted()?
# A: .sort() sorts IN PLACE and returns None. sorted() returns a NEW sorted
#    list and works on any iterable. Use sorted() when you must keep original.
#
# Q: Does list.remove() remove ALL occurrences?
# A: No. Only the FIRST matching value. Raises ValueError if not found.
#
# Q: What is the output of a = [1,2]; b = a; b.append(3); print(a)?
# A: [1, 2, 3] — aliasing. Both names refer to the same list object.
#
# Q: Are lists good for stacks/queues?
# A: Stack — yes (append/pop from end, O(1)). Queue — no (pop(0) is O(n)).
#    Use collections.deque for O(1) appends/pops from both ends.

if __name__ == "__main__":
    print("Run directly to see list examples.")
