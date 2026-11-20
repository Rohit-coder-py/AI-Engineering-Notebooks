"""
================================================================================
DAY 2 — Interview Questions (Theory + Practical)
================================================================================

INSTRUCTION: Answer each yourself FIRST. Then read the answer and run the code
snippet under each practical section.
================================================================================
"""

# ==============================================================================
# THEORY QUESTIONS
# ==============================================================================

"""
Q1. List vs Tuple — when to use which?

A: Use list for homogeneous collections that change (add/remove/reorder).
   Use tuple for fixed records, heterogeneous data, dict keys (hashable),
   and when immutability documents intent. Tuples are slightly lighter/faster.

Q2. List .sort() vs sorted()?

A: .sort() is in-place, returns None, works only on lists.
   sorted() returns a new list, works on any iterable. Original unchanged.

Q3. What is the time complexity of 'x in list' vs 'x in set' vs 'x in dict keys'?

A: list: O(n) — linear scan.   set: average O(1) — hash table lookup.
   dict keys: average O(1) — hash table lookup.

Q4. What does for-else do? When is it useful?

A: The else block runs only if the loop completed without hitting break.
   Useful for search: loop through items, break on match, else = "not found".

Q5. Are dict keys ordered? Can they be duplicated?

A: Insertion order is preserved (Python 3.7+ spec). Keys are unique —
   assigning an existing key updates its value instead of creating a duplicate.

Q6. What must dict keys / set elements be?

A: Hashable — __hash__() that never changes during lifetime + __eq__().
   Immutable built-ins qualify. Lists, dicts, sets do not.

Q7. Difference between break, continue, pass?

A: break — exits the loop entirely. continue — skips to next iteration.
   pass — does nothing; a placeholder where a statement is required syntactically.

Q8. What does zip() do if iterables differ in length?

A: Stops at the SHORTEST iterable. Use itertools.zip_longest to continue to
   the longest with a fillvalue.

Q9. What is list comprehension, and when is it preferred over a for loop?

A: [expr for item in iterable if cond] — builds a list in one readable,
   usually faster expression. Preferred for simple transformations/filters;
   use a plain for loop for complex logic.

Q10. Can a tuple be mutated? Can a tuple containing a list change?

A: Tuple itself cannot be reassigned items. But if it holds a mutable object
   (like a list), that inner object can be mutated in place.
"""

# ==============================================================================
# PRACTICAL QUESTIONS
# ==============================================================================

"""
P1. Given a list of numbers, create a new list with only even numbers squared.
    Use a list comprehension.

P2. Remove duplicates from a list while preserving original order.

P3. Merge two lists into a dictionary (keys from list1, values from list2).

P4. Count word frequencies in a sentence using a dictionary (no imports,
    then again with collections.defaultdict).

P5. Given a list of tuples (name, score), find the name with the highest score.

P6. Write a loop that prints numbers 1..20, skipping multiples of 3, and
    stops entirely at 15 (use continue and break).

P7. Demonstrate set union, intersection, and difference with two sets.
"""

# --- P1 ---
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("P1:", even_squares)   # [4, 16, 36]

# --- P2 ---
items = ["apple", "banana", "apple", "cherry", "banana", "date"]
unique_ordered = list(dict.fromkeys(items))
print("P2:", unique_ordered)   # ['apple', 'banana', 'cherry', 'date']

# --- P3 ---
keys = ["name", "age", "city"]
values = ["Rohit", 25, "Pune"]
merged = {k: v for k, v in zip(keys, values)}
print("P3:", merged)           # {'name': 'Rohit', 'age': 25, 'city': 'Pune'}

# --- P4 ---
sentence = "apple banana apple cherry banana apple"
words = sentence.split()
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
print("P4:", freq)             # {'apple': 3, 'banana': 2, 'cherry': 1}

from collections import defaultdict
freq2 = defaultdict(int)
for w in words:
    freq2[w] += 1
print("P4 defaultdict:", dict(freq2))

# --- P5 ---
students = [("Rohit", 85), ("Amit", 92), ("Sara", 78)]
top_name, top_score = max(students, key=lambda s: s[1])
print("P5:", top_name, top_score)   # Amit 92

# --- P6 ---
for i in range(1, 21):
    if i == 15:
        break
    if i % 3 == 0:
        continue
    print(i, end=" ")
print()   # 1 2 4 5 7 8 10 11 13 14

# --- P7 ---
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("P7 union:", a | b)               # {1, 2, 3, 4, 5, 6}
print("P7 intersection:", a & b)        # {3, 4}
print("P7 difference:", a - b)          # {1, 2}

if __name__ == "__main__":
    print("Day 2 interview snippets ran above.")
