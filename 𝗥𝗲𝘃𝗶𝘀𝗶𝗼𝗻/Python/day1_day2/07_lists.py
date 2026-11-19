"""
DAY 2 | 07 - LISTS
==================
Creation, indexing, slicing, methods, sorting, copying, nested lists,
comprehensions, complexity, common traps.

Run: python 07_lists.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. THEORY")
# ----------------------------------------------------------------------
# list = ordered, MUTABLE, allows duplicates, can hold mixed types.
# Internally: a dynamic array of POINTERS to objects (over-allocates for
# amortised O(1) append).
# Complexity: index O(1) | append O(1) amortised | insert/remove/pop(0) O(n)
#             'in' / index / count O(n) | sort O(n log n) | len O(1)
nums = [10, 20, 30, 40, 50]
mixed = [1, "two", 3.0, [4, 5], None]
print(nums, mixed, list(range(3)), list("hi"), [0] * 3)

# ----------------------------------------------------------------------
section("2. INDEXING & SLICING")
# ----------------------------------------------------------------------
print(nums[0], nums[-1], nums[-2])
print(nums[1:4], nums[:2], nums[3:], nums[::2], nums[::-1])
print(nums[10:20])           # slicing never raises IndexError -> []
# nums[10] -> IndexError
nums[1:3] = [21, 31, 32]     # slice assignment can change the length
print(nums)
nums[1:4] = [20, 30]
del nums[0]
print(nums)
nums = [10, 20, 30, 40, 50]

# ----------------------------------------------------------------------
section("3. ADDING / REMOVING")
# ----------------------------------------------------------------------
a = [1, 2, 3]
a.append(4)               # add one item at end
a.extend([5, 6])          # add many items
a.insert(0, 0)            # insert at index
a += [7]
print(a)
a.append([8, 9])          # appends the LIST as ONE element
print(a)
a.pop()                   # remove last, returns it
print(a.pop(0), a)        # remove by index
a.remove(3)               # remove FIRST occurrence by value (ValueError if absent)
print(a)
a.clear()
print(a)

# ----------------------------------------------------------------------
section("4. SEARCH / COUNT / SORT / REVERSE")
# ----------------------------------------------------------------------
data = [5, 2, 8, 2, 9, 1]
print(data.index(2), data.count(2), 8 in data, len(data), min(data), max(data), sum(data))
data.sort()                          # in place, returns None!
print(data)
data.sort(reverse=True)
print(data)
print(sorted(data))                  # returns NEW list, original untouched
words = ["banana", "Apple", "cherry"]
print(sorted(words), sorted(words, key=str.lower), sorted(words, key=len))
people = [("A", 25), ("B", 20), ("C", 30)]
print(sorted(people, key=lambda p: p[1]))        # sort by age
data.reverse()                       # in place
print(data, list(reversed(data)))
# Stable sort: equal keys keep original order (useful for multi-key sorts)

# ----------------------------------------------------------------------
section("5. COPYING - the classic trap")
# ----------------------------------------------------------------------
orig = [1, [2, 3]]
alias = orig                 # same object
shallow = orig[:]            # also orig.copy() or list(orig)
import copy
deep = copy.deepcopy(orig)
orig[1].append(99)
orig.append("new")
print("alias  :", alias)     # sees everything
print("shallow:", shallow)   # sees inner change, not the outer append
print("deep   :", deep)      # sees nothing

# ----------------------------------------------------------------------
section("6. NESTED LISTS & THE [[0]*3]*3 TRAP")
# ----------------------------------------------------------------------
bad = [[0] * 3] * 3          # 3 references to the SAME inner list
bad[0][0] = 1
print("bad :", bad)
good = [[0] * 3 for _ in range(3)]
good[0][0] = 1
print("good:", good)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2], [row[0] for row in matrix])
print("transpose:", [list(r) for r in zip(*matrix)])
print("flatten  :", [x for row in matrix for x in row])

# ----------------------------------------------------------------------
section("7. COMPREHENSIONS & BUILT-IN HELPERS")
# ----------------------------------------------------------------------
print([x ** 2 for x in range(6) if x % 2 == 0])
print([x if x > 0 else 0 for x in [-1, 2, -3]])     # conditional EXPRESSION (note position)
print(list(map(str.upper, ["a", "b"])), list(filter(lambda x: x > 2, [1, 2, 3, 4])))
print(list(zip([1, 2], "ab")), any([0, 1]), all([1, 1]))
first, *rest = [1, 2, 3]
print(first, rest)

# ----------------------------------------------------------------------
section("8. LIST AS STACK AND QUEUE")
# ----------------------------------------------------------------------
stack = []
stack.append(1); stack.append(2); print(stack.pop())    # LIFO
from collections import deque
q = deque([1, 2, 3])
q.append(4); print(q.popleft())          # FIFO O(1); list.pop(0) is O(n)

# ----------------------------------------------------------------------
section("9. COMMON PROBLEMS")
# ----------------------------------------------------------------------
def second_largest(nums):
    uniq = sorted(set(nums))
    return uniq[-2] if len(uniq) >= 2 else None
print(second_largest([5, 1, 9, 9, 3]))

def rotate(nums, k):
    k %= len(nums)
    return nums[-k:] + nums[:-k]
print(rotate([1, 2, 3, 4, 5], 2))

def remove_dups_keep_order(nums):
    seen, out = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out
print(remove_dups_keep_order([3, 1, 3, 2, 1]))

def two_sum(nums, target):           # O(n) using dict
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
print(two_sum([2, 7, 11, 15], 9))

def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]
print(merge_sorted([1, 4, 7], [2, 3, 9]))

# ----------------------------------------------------------------------
section("10. PREDICT THE OUTPUT")
# ----------------------------------------------------------------------
x = [1, 2, 3]
y = x
y += [4]
print(x)                       # ?
x = x + [5]
print(x, y)                    # ?
print([1, 2, 3] * 2)           # ?
print(list("abc")[::-1])       # ?
t = [3, 1, 2]
print(t.sort(), t)             # ?
def add(item, bucket=[]):      # mutable default argument trap
    bucket.append(item)
    return bucket
print(add(1), add(2))          # ?
