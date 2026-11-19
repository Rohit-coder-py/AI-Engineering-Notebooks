# Python Interview Theory Questions: Day 1 + Day 2

Try answering out loud first, then read the answer. Marked **(⭐)** = asked very frequently.

---

## A. Variables, memory, typing

**1. (⭐) What is a variable in Python? How is it different from C/Java?**
A variable is a name bound to an object in memory, not a storage box. Assignment (`x = 5`) binds the name to an object. Types belong to objects, not names, so the same name can later point to any type.

**2. (⭐) Difference between `==` and `is`?**
`==` compares values (`__eq__`). `is` compares identity (same object, `id(a) == id(b)`). Use `is` only for singletons: `None`, `True`, `False`.

**3. What does `id()` return? What is small-int caching?**
`id()` gives the object's identity (memory address in CPython). CPython pre-creates ints from -5 to 256, so `int("256") is int("256")` is `True`, but 257 usually creates separate objects. It is an implementation detail; never depend on it.

**4. (⭐) Is Python pass-by-value or pass-by-reference?**
Neither exactly: it is pass-by-object-reference (call by sharing). The function receives a reference to the same object. Mutating it (`lst.append`) affects the caller; rebinding the parameter (`lst = []`) does not.

**5. (⭐) Is Python statically or dynamically typed? Strongly or weakly?**
Dynamically typed (types checked at runtime) and strongly typed (`"5" + 5` raises `TypeError`, no silent coercion). Type hints are not enforced at runtime.

**6. What happens internally on `x = x + 1` for an int?**
A new int object is created for the result, and the name `x` is rebound to it. The old object is freed when its reference count drops to 0.

**7. How does Python manage memory?**
Reference counting plus a cyclic garbage collector for reference cycles. Objects live on a private heap managed by the interpreter.

**8. What are naming rules and conventions?**
Rules: start with letter/underscore, only letters/digits/underscore, case-sensitive, not a keyword. PEP 8: `snake_case` variables/functions, `UPPER_CASE` constants, `PascalCase` classes, `_internal`.

**9. What does `a = b = []` do?**
Both names point to the same list; modifying one shows in the other. `a, b = [], []` creates two lists.

**10. How do you swap two variables?**
`a, b = b, a` (the right side tuple is built first, then unpacked).

**11. What does `del x` do?**
Removes the name `x` from the namespace (decrements refcount). It does not directly delete the object.

**12. What is the difference between shallow and deep copy?**
Shallow copy duplicates the outer container but shares inner objects. Deep copy (`copy.deepcopy`) recursively copies everything.

---

## B. Data types and conversion

**13. (⭐) Mutable vs immutable types? Examples.**
Mutable: list, dict, set, bytearray. Immutable: int, float, bool, str, tuple, frozenset, bytes, None. Immutable "changes" create new objects.

**14. (⭐) Why is `0.1 + 0.2 != 0.3`? How do you fix it?**
Floats use binary IEEE 754, and 0.1/0.2 can't be represented exactly. Use `math.isclose()` for comparison or `decimal.Decimal` for exact decimals (money).

**15. Is `bool` a subclass of `int`?**
Yes. `True == 1`, `True + True == 2`, `isinstance(True, int)` is `True`.

**16. (⭐) List the falsy values.**
`False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)`, and objects whose `__bool__` returns False or `__len__` returns 0.

**17. `int(3.9)` vs `round(3.9)` vs `math.floor`?**
`int` truncates toward zero (3, and -3 for -3.9), `round` rounds to nearest with banker's rounding (`round(2.5) == 2`), `floor` goes toward -∞.

**18. Why does `int("3.5")` fail?**
`int()` on a string only accepts integer literals. Use `int(float("3.5"))`.

**19. What does `input()` return?**
Always `str`. Convert explicitly.

**20. `type()` vs `isinstance()`?**
`isinstance` respects inheritance and accepts tuples of types; `type(x) == T` is an exact match. Prefer `isinstance`.

**21. Are strings mutable? How do you build strings efficiently?**
Immutable. Repeated `+=` in a loop can be O(n²); collect pieces in a list and `"".join(parts)`.

**22. Python int overflow?**
Python ints have arbitrary precision; no overflow (only memory limits).

**23. `bool("False")`?**
`True`. Any non-empty string is truthy.

---

## C. Operators

**24. (⭐) `/` vs `//` vs `%`. What is `-7 // 2` and `-7 % 2`?**
`/` true division (float), `//` floor division, `%` remainder. `-7 // 2 == -4`, `-7 % 2 == 1` (floor semantics; invariant `a == (a//b)*b + a%b`).

**25. (⭐) What do `and`/`or` return?**
Operands, not booleans. `a and b` returns first falsy else last; `a or b` returns first truthy else last. `x or "default"` is a common idiom.

**26. What is short-circuit evaluation?**
`and`/`or` stop evaluating as soon as the result is known. `x != 0 and 10/x > 1` avoids division by zero.

**27. What is operator precedence of `not`, `and`, `or`?**
`not` > `and` > `or`. `True or False and False` is `True`.

**28. What does `2 ** 3 ** 2` give?**
512, because `**` is right-associative (`2 ** 9`).

**29. What is the walrus operator?**
`:=` assigns inside an expression: `if (n := len(a)) > 10:`.

**30. `in` on dict, list, set, str: what does it check?**
dict → keys; list/tuple → items (O(n)); set → items (O(1) avg); str → substring.

---

## D. Conditionals and loops

**31. (⭐) Difference between `break`, `continue`, `pass`?**
`break` exits the loop, `continue` skips to the next iteration, `pass` is a no-op placeholder.

**32. (⭐) What is `for ... else`?**
`else` runs only if the loop completed without `break`. Useful in searches (e.g., prime check).

**33. When use `for` vs `while`?**
`for` when iterating a known iterable/count; `while` when the number of iterations depends on a condition.

**34. How does a `for` loop work internally?**
Calls `iter()` on the iterable to get an iterator, then repeatedly calls `next()` until `StopIteration`.

**35. `range()` in Python 3: list or not?**
A lazy immutable sequence object (O(1) memory); supports `len`, indexing, `in`, slicing.

**36. Why not modify a list while iterating over it?**
Indices shift and elements get skipped. Iterate over a copy or build a new list (comprehension).

**37. `enumerate` and `zip`: what are they for?**
`enumerate` gives (index, item); `zip` pairs iterables, stopping at the shortest (`zip_longest` pads).

**38. What is a ternary expression?**
`value_if_true if cond else value_if_false`.

**39. What is `match-case`?**
Structural pattern matching (3.10+), more powerful than switch: literals, `|`, sequences, guards `case x if ...`, wildcard `_`.

**40. List vs generator expression?**
`[x for ...]` builds the full list in memory; `(x for ...)` lazily yields one at a time.

---

## E. Lists

**41. (⭐) List vs tuple?**
List: mutable, dynamic, for homogeneous growing data. Tuple: immutable, hashable if items are, smaller/faster, for fixed records and dict keys.

**42. (⭐) `append` vs `extend` vs `insert`?**
`append(x)` adds one item (a list becomes a nested element), `extend(it)` adds each item, `insert(i, x)` inserts at an index (O(n)).

**43. (⭐) `sort()` vs `sorted()`?**
`list.sort()` sorts in place and returns `None`; `sorted()` returns a new list and works on any iterable. Both are stable (Timsort, O(n log n)).

**44. (⭐) Time complexity of list operations?**
index/len/append(amortised): O(1); insert/delete at front, `in`, `index`, `count`, `remove`: O(n); sort: O(n log n).

**45. How do you copy a list?**
`lst.copy()`, `lst[:]`, `list(lst)` (shallow); `copy.deepcopy(lst)` for nested.

**46. What's wrong with `[[0]*3]*3`?**
It creates 3 references to the same inner list. Use `[[0]*3 for _ in range(3)]`.

**47. `remove` vs `pop` vs `del`?**
`remove(value)` first match (ValueError if none); `pop(i)` by index and returns it; `del lst[i]`/slices removes without returning.

**48. How is a list implemented internally?**
A dynamic array of pointers that over-allocates, giving amortised O(1) append.

**49. Why is `list.pop(0)` slow, and what to use instead?**
All remaining items shift: O(n). Use `collections.deque.popleft()` (O(1)).

**50. What is the mutable default argument bug?**
`def f(x, bucket=[])` creates the list once at function definition, shared across calls. Use `bucket=None` then `bucket = [] if bucket is None else bucket`.

---

## F. Tuples

**51. (⭐) Why use tuples if lists exist?**
Immutability (safety), hashability (dict keys/set members), slightly less memory and faster, semantic meaning of a fixed record.

**52. How to create a one-element tuple?**
`(5,)` or `5,`. `(5)` is just an int.

**53. Can a tuple contain a list? Can you modify it?**
Yes; the tuple can't change which objects it holds, but the list inside is still mutable. Such a tuple is unhashable.

**54. What is tuple packing/unpacking?**
`t = 1, 2, 3` packs; `a, b, c = t` unpacks; `a, *rest = t` collects extras into a list.

**55. What is `namedtuple`?**
A tuple subclass with named fields: readable, immutable records (`p.x`, `p[0]`).

---

## G. Sets

**56. (⭐) What is a set? Properties?**
Unordered collection of unique hashable elements, backed by a hash table: O(1) average add/remove/membership.

**57. (⭐) How do you make an empty set?**
`set()`. `{}` creates an empty dict.

**58. Set operations?**
union `|`, intersection `&`, difference `-`, symmetric difference `^`, subset `<=`, superset `>=`, `isdisjoint`.

**59. `remove` vs `discard`?**
`remove` raises `KeyError` if missing; `discard` doesn't.

**60. `set` vs `frozenset`?**
`frozenset` is immutable and hashable (can be a dict key or set element).

**61. Why can't a set hold a list?**
Lists are unhashable (mutable). Use a tuple or frozenset.

**62. Remove duplicates while keeping order?**
`list(dict.fromkeys(items))`. `list(set(items))` loses order.

---

## H. Dictionaries

**63. (⭐) How does a dict work internally?**
Hash table: key → `hash()` → slot lookup. Collisions handled by open addressing. Average O(1) get/set/delete; worst case O(n). Keys must be hashable and have consistent `__eq__`/`__hash__`.

**64. (⭐) Are dicts ordered?**
Yes, insertion-ordered since Python 3.7 (implementation in 3.6).

**65. (⭐) `d[key]` vs `d.get(key)`?**
`d[key]` raises `KeyError` if missing; `get` returns `None` (or a default).

**66. What can be a dict key?**
Any hashable object: int, str, tuple of hashables, frozenset, bool. Not list/dict/set.

**67. `setdefault` vs `defaultdict`?**
`setdefault(k, v)` is per-call; `defaultdict(factory)` auto-creates missing values on access.

**68. How to merge two dicts?**
`a | b` (3.9+), `{**a, **b}`, `a.update(b)`; right-hand values win on conflicts.

**69. How to sort a dict by value?**
`dict(sorted(d.items(), key=lambda kv: kv[1]))`.

**70. How to iterate with keys and values?**
`for k, v in d.items():`

**71. `dict.keys()` returns a list?**
No, a dynamic view object that reflects later changes and supports set-like operations.

**72. Why does `{1: "a", True: "b", 1.0: "c"}` have one key?**
`1 == True == 1.0` and they hash equally, so they're the same key (value overwritten, first key object kept).

**73. `Counter` use?**
Counting hashables; `most_common(n)`, arithmetic between counters.

**74. Dict vs list for lookups?**
Dict gives O(1) lookup by key; list needs O(n) search. Trade-off is memory.

**75. What is a hashable object?**
Has a `__hash__` that never changes during its lifetime and `__eq__`; immutable built-ins are hashable, mutable containers are not.

---

## I. Rapid-fire (one-liners)

| Question | Answer |
|---|---|
| Python's `None` type? | `NoneType`, a singleton |
| Index of last item? | `-1` |
| Reverse a string? | `s[::-1]` |
| Check if list empty? | `if not lst:` |
| Count items in list? | `len(lst)` / `lst.count(x)` |
| Get unique sorted items? | `sorted(set(x))` |
| Convert list of str → int? | `list(map(int, lst))` |
| Is a string palindrome? | `s == s[::-1]` |
| Max by custom key? | `max(items, key=...)` |
| Flatten 2D list? | `[x for row in m for x in row]` |
| Check all/any? | `all(...)`, `any(...)` |
| Swap dict keys/values? | `{v: k for k, v in d.items()}` |
| Is Python compiled or interpreted? | Source → bytecode (`.pyc`) → run by the PVM; so both |
| What is PEP 8? | Official style guide |
| Which is faster for membership: list or set? | set |
