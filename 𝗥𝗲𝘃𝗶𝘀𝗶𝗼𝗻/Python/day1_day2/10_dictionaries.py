"""
DAY 2 | 10 - DICTIONARIES
========================
Creation, access, methods, iteration, comprehensions, nesting, merging,
defaultdict/Counter, sorting, common patterns.

Run: python 10_dictionaries.py
"""


def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ----------------------------------------------------------------------
section("1. THEORY")
# ----------------------------------------------------------------------
# dict = mapping of unique, HASHABLE keys -> values. Mutable.
# Hash table internally: lookup/insert/delete O(1) average.
# Since Python 3.7 dicts PRESERVE INSERTION ORDER (language guarantee).
# Keys: int, str, tuple(of hashables), frozenset, bool... never list/dict/set.
d = {"name": "Harsh", "age": 19, "skills": ["python", "sql"]}
print(d, len(d), type(d))
print(dict(a=1, b=2), dict([("x", 1), ("y", 2)]), dict(zip("ab", [1, 2])))
print(dict.fromkeys(["a", "b"], 0), {})
print({1: "int", "1": "str", 1.0: "float?"})   # 1 and 1.0 are the SAME key

# ----------------------------------------------------------------------
section("2. ACCESS")
# ----------------------------------------------------------------------
print(d["name"])
try:
    d["email"]
except KeyError as e:
    print("KeyError:", e)
print(d.get("email"))               # None, no error
print(d.get("email", "not given"))  # custom default
print("name" in d, "Harsh" in d)    # membership checks KEYS

# ----------------------------------------------------------------------
section("3. ADD / UPDATE / DELETE")
# ----------------------------------------------------------------------
d["city"] = "Varanasi"                  # add
d["age"] = 20                           # update
d.update({"age": 21, "college": "BCA"}) # bulk (also d.update(age=22))
print(d)
print(d.pop("college"))                 # remove, returns value
print(d.pop("nope", "default"))         # safe pop
print(d.popitem())                      # removes LAST inserted pair -> ('city', 'Varanasi')
del d["skills"]                         # del: remove by key, raises KeyError if missing
print(d)
# setdefault: get value, inserting default if missing
d.setdefault("country", "India")
d.setdefault("country", "xx")           # does nothing now
print(d)
d.clear()
print(d)

# ----------------------------------------------------------------------
section("4. VIEWS & ITERATION")
# ----------------------------------------------------------------------
marks = {"math": 90, "sci": 80, "eng": 70}
print(marks.keys(), marks.values(), marks.items())     # dynamic VIEW objects
for k in marks: print(k, end=" ")
print()
for k, v in marks.items(): print(f"{k}={v}", end=" ")
print()
print(list(marks), sum(marks.values()), max(marks, key=marks.get))
# Don't change dict SIZE while iterating (RuntimeError). Iterate a copy:
for k in list(marks):
    if marks[k] < 75:
        del marks[k]
print(marks)

# ----------------------------------------------------------------------
section("5. COMPREHENSIONS, MERGE, COPY")
# ----------------------------------------------------------------------
print({x: x ** 2 for x in range(5)})
print({k: v for k, v in {"a": 1, "b": 2, "c": 3}.items() if v > 1})
inv = {v: k for k, v in {"a": 1, "b": 2}.items()}      # invert (values must be unique/hashable)
print(inv)

a, b = {"x": 1, "y": 2}, {"y": 20, "z": 30}
print(a | b)                  # 3.9+: right side wins
print({**a, **b})             # older style
a |= b
print(a)

orig = {"nums": [1, 2]}
shallow = orig.copy()
import copy
deep = copy.deepcopy(orig)
orig["nums"].append(3)
print(shallow, deep)

# ----------------------------------------------------------------------
section("6. NESTED DICTIONARIES")
# ----------------------------------------------------------------------
students = {
    101: {"name": "Asha", "marks": {"math": 90, "sci": 85}},
    102: {"name": "Ravi", "marks": {"math": 70, "sci": 95}},
}
print(students[101]["marks"]["math"])
print(students.get(103, {}).get("name", "unknown"))     # safe chain
students[102]["marks"]["eng"] = 88
for roll, info in students.items():
    avg = sum(info["marks"].values()) / len(info["marks"])
    print(roll, info["name"], round(avg, 2))

# ----------------------------------------------------------------------
section("7. defaultdict & Counter")
# ----------------------------------------------------------------------
from collections import defaultdict, Counter
groups = defaultdict(list)
for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
    groups[word[0]].append(word)         # no key check needed
print(dict(groups))

counts = defaultdict(int)
for ch in "mississippi":
    counts[ch] += 1
print(dict(counts))

c = Counter("mississippi")
print(c, c.most_common(2), c["z"])       # missing -> 0
print(Counter([1, 1, 2]) + Counter([2, 3]))

# ----------------------------------------------------------------------
section("8. SORTING DICTS")
# ----------------------------------------------------------------------
scores = {"A": 82, "B": 95, "C": 70}
print(sorted(scores))                                       # keys
print(sorted(scores.items(), key=lambda kv: kv[1], reverse=True))
print(dict(sorted(scores.items(), key=lambda kv: kv[1])))   # new dict ordered by value
print(max(scores, key=scores.get), min(scores.values()))

# ----------------------------------------------------------------------
section("9. COMMON PATTERNS")
# ----------------------------------------------------------------------
def char_freq(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq
print(char_freq("banana"))

def first_unique_char(s):
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1
print(first_unique_char("leetcode"), first_unique_char("aabb"))

def group_anagrams(words):
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return list(g.values())
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
print(two_sum([3, 2, 4], 6))

# memoization with a dict
cache = {}
def fib(n):
    if n < 2: return n
    if n not in cache:
        cache[n] = fib(n - 1) + fib(n - 2)
    return cache[n]
print(fib(50))

# ----------------------------------------------------------------------
section("10. PREDICT THE OUTPUT")
# ----------------------------------------------------------------------
d = {1: "a", True: "b", 1.0: "c"}
print(d, len(d))                         # ?
d = {"a": 1}
d2 = d
d2["b"] = 2
print(d)                                 # ?
print({"a": 1}.get("b", 0) + 1)          # ?
print(list({"x": 1, "y": 2}.items())[0]) # ?
print("a" in {"a": None})                # ?
x = dict.fromkeys(range(3), [])
x[0].append(1)
print(x)                                 # ?  (shared list trap)
