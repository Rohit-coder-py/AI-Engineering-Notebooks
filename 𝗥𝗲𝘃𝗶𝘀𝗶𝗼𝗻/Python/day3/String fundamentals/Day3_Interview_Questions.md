# Python Mastery — Day 3
## Strings, Functions & Reusable Code — Complete Interview Question Bank

> **Date:** November 21, 2026
> **Folder:** `Revision/Python/day3/String fundamentals/`
> **Companion files:** `01`–`10` Python lessons, project, and practical interview drills.
> **How to use:** Cover the answer, answer aloud, then compare. Aim for **direct answer → reason → example**.

---

## Legend

| Tag | Meaning |
|---|---|
| `[Basic]` | Screening / fundamentals. Must answer instantly. |
| `[Intermediate]` | Standard first-round depth. |
| `[Advanced]` | Differentiator; expect follow-ups. |
| `[Trap]` | Common wrong answer; interviewers use it to test precision. |

**Framework for every answer**

1. **Direct answer** — one sentence.
2. **Mechanism** — why Python behaves that way.
3. **Example** — a tiny snippet or output.
4. **Caveat** — edge case or trade-off (only if relevant).

---

## Table of Contents

1. [Strings — Fundamentals](#1-strings--fundamentals)
2. [Strings — Common Methods](#2-strings--common-methods)
3. [Strings — Membership, Escapes, Comparison, Unicode](#3-strings--membership-escapes-comparison-unicode)
4. [Functions — Fundamentals](#4-functions--fundamentals)
5. [Function Arguments](#5-function-arguments)
6. [Scope, LEGB, Closures](#6-scope-legb-closures)
7. [Lambda, map, filter, sorted, Documentation, Typing](#7-lambda-map-filter-sorted-documentation-typing)
8. [Function Design & Side Effects](#8-function-design--side-effects)
9. [Recursion](#9-recursion)
10. [Output Prediction Drills](#10-output-prediction-drills)
11. [Debugging & Code Review Drills](#11-debugging--code-review-drills)
12. [Coding Challenges with Solutions](#12-coding-challenges-with-solutions)
13. [Rapid-Fire One-Liners](#13-rapid-fire-one-liners)
14. [Behavioural & Communication Questions](#14-behavioural--communication-questions)
15. [45-Minute Mock Interview Plan](#15-45-minute-mock-interview-plan)
16. [Self-Scoring Rubric](#16-self-scoring-rubric)

---

# 1. Strings — Fundamentals

### Q1. What is a Python string? `[Basic]`

**Answer.** An **immutable sequence of Unicode code points**. It supports indexing, slicing, `len()`, iteration, and membership because it implements the sequence protocol.

**Say this too:** There is no separate `char` type — `s[0]` returns a new one-character `str`.

---

### Q2. Are strings mutable? `[Basic]`

**Answer.** No. Item assignment raises `TypeError: 'str' object does not support item assignment`. Any "change" creates a new string object and rebinds the name.

```python
s = "rohit"
# s[0] = "R"          # TypeError
s = "R" + s[1:]       # new object, s rebound
```

**Follow-up:** Why does `s += "x"` work? Because `+=` on an immutable type is **reassignment**: `s = s + "x"`.

---

### Q3. Why is string immutability useful? `[Intermediate]`

**Answer.**

1. **Hashable** → safe as dict keys and set members.
2. **Safe sharing** → passing a string to a function cannot corrupt the caller.
3. **Thread-friendly** → immutable data needs no locking.
4. **Interning** → identical literals can share one object, making equality checks fast.

---

### Q4. How do you create a string? `[Basic]`

**Answer.** Literals (`'x'`, `"x"`, `'''...'''`), `str(obj)`, `"".join(parts)`, decoded bytes (`b"...".decode("utf-8")`), and adjacent literal concatenation.

```python
name = "Rohit"
text = str(42)
path = "".join(["a", "/", "b"])
```

**Trap:** Adjacent-literal concatenation only works for **literals**, not variables: `("a" "b")` works; `(x y)` is a syntax error.

---

### Q5. Explain positive and negative indexing. `[Basic]`

**Answer.** Indexing is 0-based from the left. Negative indexes count from the right: `-1` is the last item, `-len(s)` is the first.

```python
s = "Python"
s[0]    # 'P'
s[-1]   # 'n'
s[-6]   # 'P'
```

Out-of-range indexing raises `IndexError`.

---

### Q6. What is the difference between `s[0]` and `s[0:1]`? `[Trap]`

**Answer.** Both return a one-character string. `s[0]` is an **index lookup**; `s[0:1]` is a **slice**. Slicing never raises `IndexError` and always returns a new string.

---

### Q7. Explain slicing rules. `[Basic]`

**Answer.** `s[start:stop:step]`

- `start` inclusive, `stop` exclusive.
- Any part may be omitted.
- Bounds are **clamped** — no `IndexError`.
- Negative `step` walks backwards.
- A slice always returns a **new** string.

```python
s = "Python"
s[1:4]    # 'yth'
s[:3]     # 'Pyt'
s[3:]     # 'hon'
s[::2]    # 'Pto'
s[::-1]   # 'nohtyP'
s[10:20]  # ''  (no error)
```

---

### Q8. How do you reverse a string? `[Basic]`

**Answer.** `s[::-1]` is idiomatic. Alternative: `"".join(reversed(s))`.

**Advanced caveat:** This reverses **code points**, not grapheme clusters. Combining accents and emoji ZWJ sequences can break. Production text handling needs a grapheme-aware library.

---

### Q9. What does `len()` return for a string? `[Intermediate]`

**Answer.** The number of **Unicode code points**, not bytes and not visible characters.

```python
len("abc")        # 3
len("e\u0301")    # 2  (e + combining accent)
len("café")       # 4  (if precomposed)
len("café".encode("utf-8"))  # 5
```

---

### Q10. What is the difference between `str` and `bytes`? `[Intermediate]`

**Answer.** `str` is Unicode text (code points). `bytes` is an immutable sequence of raw byte values (0–255). Convert with `encode()` / `decode()`, normally UTF-8. Concatenating them raises `TypeError`.

```python
data = "café".encode("utf-8")   # b'caf\xc3\xa9'
text = data.decode("utf-8")     # 'café'
```

---

### Q11. Is Unicode the same as UTF-8? `[Intermediate]`

**Answer.** No. **Unicode** is the character/code-point standard. **UTF-8** is one *encoding* of code points into bytes (1–4 bytes each). Python `str` stores code points; encoding matters for files, network, and databases.

---

### Q12. What is string concatenation and repetition? `[Basic]`

**Answer.** `+` joins two strings; `*` repeats a string by an integer.

```python
"Ada" + " " + "Lovelace"   # 'Ada Lovelace'
"-" * 5                    # '-----'
"hi" * 0                   # ''
```

`"Age: " + 25` raises `TypeError`; use `str(25)` or an f-string.

---

### Q13. Why is `+=` in a loop a performance problem? `[Advanced]`

**Answer.** Strings are immutable, so each `+=` conceptually copies the accumulated text → **O(n²)**. Collect parts and call `"".join(parts)` once → **O(n)**.

**Nuance:** CPython may resize in place when the string's refcount is 1, but that is an implementation detail — never rely on it.

---

### Q14. Compare f-strings, `format()`, and `%` formatting. `[Basic]`

**Answer.**

| Style | Example | When to use |
|---|---|---|
| f-string | `f"{name}: {score:.2f}"` | Default choice; readable and fast |
| `format()` | `"{}: {:.2f}".format(name, score)` | Template is data/reused |
| `%` | `"%s: %.2f" % (name, score)` | Legacy code, lazy logging |

All return a new string; none mutate the template.

---

### Q15. Show useful f-string format specs. `[Intermediate]`

**Answer.**

```python
f"{3.14159:.2f}"     # '3.14'
f"{42:05d}"          # '00042'
f"{1234567:,}"       # '1,234,567'
f"{0.873:.1%}"       # '87.3%'
f"{'x':^7}"          # '   x   '
f"{name!r}"          # repr
f"{age=}"            # 'age=25' (debug form)
```

Grammar: `[[fill]align][sign][#][0][width][grouping][.precision][type]`.

---

### Q16. Why does logging prefer `%`-style over f-strings? `[Advanced]`

**Answer.** f-strings are evaluated **eagerly**, even if the log record is discarded. `logger.info("x=%s", x)` formats **lazily**, only when that level is enabled. Use lazy `%`-style for hot or debug logging.

---

### Q17. Are f-strings evaluated when defined or when used? `[Intermediate]`

**Answer.** Immediately, when the line executes — unlike a lambda body or a `%`-format string passed to logging.

---

### Q18. What is a triple-quoted string used for? `[Basic]`

**Answer.** Multi-line text and **docstrings**. If it is the first statement in a module, function, or class, Python stores it in `__doc__`.

---

# 2. Strings — Common Methods

### Q19. Difference between `lower()`, `upper()`, `title()`, `capitalize()`, `swapcase()`? `[Basic]`

**Answer.**

```python
"PyThOn".lower()       # 'python'
"python".upper()       # 'PYTHON'
"hello world".title()  # 'Hello World'
"hELLO".capitalize()   # 'Hello'
"PyThOn".swapcase()    # 'pYtHoN'
```

`title()` capitalizes every word; `capitalize()` only the first character and lowercases the rest.

---

### Q20. What is the `title()` gotcha? `[Trap]`

**Answer.** Word boundaries are **non-letters**, so apostrophes split words:

```python
"it's a test".title()   # "It'S A Test"
```

For names, split and capitalize manually.

---

### Q21. Difference between `lower()` and `casefold()`? `[Intermediate]`

**Answer.** `lower()` is simple lowercasing for display. `casefold()` is aggressive Unicode **caseless matching**.

```python
"STRASSE".casefold() == "straße".casefold()   # True
"STRASSE".lower() == "straße".lower()         # False
```

Use `casefold()` for comparisons and searches.

---

### Q22. Explain `strip()`, `lstrip()`, `rstrip()`. `[Basic]`

**Answer.** They remove characters from the ends. With no argument they remove whitespace; with an argument they treat it as a **character set**, not a prefix.

```python
"  x  ".strip()          # 'x'
"xxhixx".strip("x")      # 'hi'
"banana".strip("ab")     # 'nan'  (stops at 'n')
```

---

### Q23. How do you remove a prefix or suffix? `[Trap]`

**Answer.** Use `removeprefix()` / `removesuffix()` (3.9+), not `strip()`.

```python
"unhappy".removeprefix("un")   # 'happy'
"file.txt".removesuffix(".txt")# 'file'
```

`strip("un")` would remove any `u`/`n` from both ends.

---

### Q24. Difference between `split()` and `split(" ")`? `[Trap]`

**Answer.** No argument splits on **runs of whitespace** and drops empty strings. An explicit separator splits on every occurrence and keeps empties.

```python
" a  b ".split()      # ['a', 'b']
" a  b ".split(" ")   # ['', 'a', '', 'b', '']
```

---

### Q25. What do `maxsplit` and `rsplit()` do? `[Intermediate]`

**Answer.** `maxsplit` limits the number of splits; the remainder stays in one piece. `rsplit()` splits from the right.

```python
"a,b,c,d".split(",", 2)    # ['a', 'b', 'c,d']
"a,b,c,d".rsplit(",", 2)   # ['a,b', 'c', 'd']
```

---

### Q26. What does `splitlines()` do? `[Basic]`

**Answer.** Splits on line boundaries and drops the newline characters by default. Handles `\n`, `\r\n`, and `\r`.

```python
"a\nb\r\nc".splitlines()   # ['a', 'b', 'c']
```

---

### Q27. How does `join()` work and what are its requirements? `[Basic]`

**Answer.** Called on the **separator**: `sep.join(iterable)`. Every element must be `str`, otherwise `TypeError`. It is O(n) and preferred over repeated `+`.

```python
",".join(["a", "b"])              # 'a,b'
",".join(str(n) for n in [1, 2])  # '1,2'
```

---

### Q28. Explain `replace()`. `[Basic]`

**Answer.** `s.replace(old, new[, count])` replaces **all** occurrences by default, is case-sensitive, and processes matches left to right **non-overlapping**.

```python
"aaa".replace("aa", "b")          # 'ba'
"banana".replace("a", "o", 2)     # 'bonona'
```

Returns a new string.

---

### Q29. Difference between `find()` and `index()`? `[Basic]`

**Answer.** Both return the first index of a substring. `find()` returns `-1` when absent; `index()` raises `ValueError`. Use `find()` when absence is normal, `index()` when absence is a bug, and `in` when you only need a boolean.

---

### Q30. Difference between `find()` and `rfind()`? `[Basic]`

**Answer.** `find()` returns the **lowest** index; `rfind()` returns the **highest** index. Both return `-1` if absent.

---

### Q31. Does `count()` count overlapping occurrences? `[Trap]`

**Answer.** No.

```python
"aaa".count("aa")   # 1
"aaaa".count("aa")  # 2
"abc".count("")     # 4  (len + 1)
```

---

### Q32. How do `startswith()` and `endswith()` handle multiple options? `[Intermediate]`

**Answer.** Pass a **tuple**:

```python
filename.endswith((".csv", ".xlsx"))
name.startswith(("Mr.", "Ms.", "Dr."))
```

Optional `start`/`end` arguments follow slice rules.

---

### Q33. Difference between `in` and `startswith()`? `[Trap]`

**Answer.** `"bc" in "abc"` is a **substring anywhere** check → `True`. `"abc".startswith("bc")` checks only the prefix → `False`.

---

### Q34. What do the `is*` methods check? `[Intermediate]`

**Answer.** Character-class predicates: `isalpha()`, `isdigit()`, `isalnum()`, `isspace()`, `isupper()`, `islower()`, `istitle()`, `isidentifier()`, `isdecimal()`, `isnumeric()`.

**Numeric subtlety:** `"²".isdigit()` is `True`, but `int("²")` fails. Prefer `isdecimal()` before `int()`, or use `try/except ValueError`.

---

### Q35. How do you pad or align strings? `[Basic]`

**Answer.**

```python
"42".zfill(5)          # '00042'
"-42".zfill(5)         # '-0042'
"hi".ljust(6, ".")     # 'hi....'
"hi".rjust(6, ".")     # '....hi'
"hi".center(10, "-")   # '----hi----'
```

---

### Q36. What is `partition()`? `[Intermediate]`

**Answer.** Splits into a 3-tuple `(before, separator, after)`. If the separator is absent, returns `(original, '', '')`. `rpartition()` splits from the right.

```python
"user@example.com".partition("@")
# ('user', '@', 'example.com')
```

---

### Q37. What are `maketrans()` and `translate()`? `[Advanced]`

**Answer.** `str.maketrans()` builds a translation table; `translate()` applies it character-by-character. Faster than many `replace()` calls.

```python
table = str.maketrans({"a": "4", "e": "3"})
"elite".translate(table)   # '3l1t3'
```

---

### Q38. How do you remove punctuation from text? `[Intermediate]`

**Answer.** Several options, with trade-offs:

```python
import string
text.translate(str.maketrans("", "", string.punctuation))  # remove all
"".join(ch for ch in text if ch not in string.punctuation)  # explicit
```

For Unicode punctuation, use `unicodedata.category(ch).startswith("P")`.

---

### Q39. How do you remove all whitespace? `[Basic]`

**Answer.** `"".join(s.split())` removes all whitespace and collapses the rest. `s.replace(" ", "")` only removes literal spaces, not tabs/newlines.

---

### Q40. Are string methods in-place? `[Trap]`

**Answer.** No. Strings are immutable, so every method returns a new string (or a list/int). This is a common "spot the bug" question:

```python
name = "rohit"
name.upper()        # returns 'ROHIT' but is discarded
print(name)         # 'rohit'
```

---

### Q41. How do you perform a case-insensitive search? `[Intermediate]`

**Answer.** Normalize both sides with `casefold()`:

```python
needle.casefold() in haystack.casefold()
```

For Unicode correctness, also normalize with `unicodedata.normalize("NFC", ...)`.

---

### Q42. How do you capitalize every word without `title()`? `[Intermediate]`

**Answer.**

```python
" ".join(w[:1].upper() + w[1:].lower() for w in text.split())
```

This avoids the apostrophe behavior of `title()` and gives control over delimiters.

---

# 3. Strings — Membership, Escapes, Comparison, Unicode

### Q43. What does `in` do for strings? `[Basic]`

**Answer.** Case-sensitive **substring** membership with no word boundaries: `"ana" in "banana"` is `True`. To check words, tokenize first.

**Complexity:** Not O(1). CPython uses an efficient search algorithm, but conceptually it scans the text.

---

### Q44. Is `"" in "abc"` true? `[Trap]`

**Answer.** Yes. The empty string is a substring of every string. `"abc".find("")` is `0`; `"abc".count("")` is `4` (`len + 1`).

---

### Q45. Name the common escape sequences. `[Basic]`

**Answer.**

| Escape | Meaning |
|---|---|
| `\n` | newline |
| `\t` | tab |
| `\\` | backslash |
| `\'` `\"` | quotes |
| `\r` | carriage return |
| `\0` | null |
| `\xhh` | hex byte |
| `\uXXXX` | 4-digit Unicode |
| `\UXXXXXXXX` | 8-digit Unicode |
| `\N{NAME}` | Unicode by name |

`len("\n")` is `1`: it is one character at runtime.

---

### Q46. What is a raw string? Does it change the type? `[Intermediate]`

**Answer.** `r"..."` stops the **parser** from interpreting backslash escapes. The runtime type is still `str`; backslashes remain literal. Common for regex and Windows paths.

```python
r"\n"        # backslash + n, length 2
re.findall(r"\d+", text)
```

**Limitations:**

1. Cannot end with an odd number of backslashes: `r"abc\"` is a syntax error.
2. Raw strings do not disable quote escaping.
3. They prevent double-escaping; they do not make regex trivial.

---

### Q47. Can you combine raw and f-strings? `[Intermediate]`

**Answer.** Yes: `rf"path\{name}"` or `fr"..."`. Braces still interpolate; backslashes stay literal.

---

### Q48. How are strings compared? `[Intermediate]`

**Answer.** **Lexicographically by Unicode code point.** Compare the first differing character; a prefix is smaller than the longer string.

```python
"apple" < "banana"   # True
"app" < "apple"      # True
"Z" < "a"            # True  (90 < 97)
"10" < "9"           # True  (string comparison, not numeric)
```

---

### Q49. Why is `"Z" < "a"` true? `[Trap]`

**Answer.** Comparison uses code points. `ord("Z") == 90`, `ord("a") == 97`, so `"Z"` sorts before `"a"`.

---

### Q50. How do you compare strings case-insensitively? `[Basic]`

**Answer.** `a.casefold() == b.casefold()`. For sorting: `sorted(words, key=str.casefold)`. For Unicode, normalize first.

---

### Q51. Is Python string comparison locale-aware? `[Advanced]`

**Answer.** No. It is code-point order, not human-language collation. For locale-aware sorting use `locale.strxfrm` or a library such as PyICU.

---

### Q52. Difference between `==` and `is` for strings? `[Trap]`

**Answer.** `==` compares **values**; `is` compares **object identity**. CPython interns some literals, so `is` may accidentally be `True`. Always use `==`; reserve `is` for `None`, `True`, `False`, and sentinels.

---

### Q53. What is string interning? `[Advanced]`

**Answer.** CPython may reuse one object for identical strings (especially short/identifier-like literals or compile-time constants). This saves memory and speeds equality, but it is an implementation detail — never depend on identity.

---

### Q54. What is Unicode normalisation and why does it matter? `[Advanced]`

**Answer.** Visually identical text can have different code-point sequences:

- Composed: `é` = `\u00e9` (1 code point)
- Decomposed: `e` + `\u0301` (2 code points)

Normalize before comparing/storing:

```python
unicodedata.normalize("NFC", text)
```

NFC is the usual choice for storage; NFD is useful for some text processing.

---

### Q55. Why can `len()` differ from the number of visible characters? `[Advanced]`

**Answer.** `len()` counts code points. Combining marks, skin-tone modifiers, flags, and emoji ZWJ sequences use multiple code points for one grapheme cluster. Example: a family emoji can be 5 code points but one visible glyph.

---

### Q56. What are `encode()` error handlers? `[Advanced]`

**Answer.** `str.encode(encoding, errors=...)` and `bytes.decode(...)` accept `strict` (default), `ignore`, `replace`, `backslashreplace`, etc.

```python
b"caf\xe9".decode("utf-8", errors="replace")  # replacement char
b"caf\xe9".decode("latin-1")                  # 'café'
```

Use explicit encodings; never rely on the platform default.

---

### Q57. What is `ord()` / `chr()`? `[Basic]`

**Answer.** Convert between a one-character string and its integer code point.

```python
ord("A")    # 65
chr(65)     # 'A'
hex(ord("A"))  # '0x41'
```

---

### Q58. How do you check if a string is ASCII? `[Intermediate]`

**Answer.** `s.isascii()` (3.7+). `ascii(s)` gives an ASCII-only `repr` with escapes.

---

# 4. Functions — Fundamentals

### Q59. What is a function and why use one? `[Basic]`

**Answer.** A **named, callable object** encapsulating behaviour, with parameters, a body, and a return value. Benefits: abstraction, reuse, testability, local scope, and easier debugging.

**Strong phrasing:** "Functions are first-class objects in Python — they can be assigned, passed, returned, and stored."

---

### Q60. What is the difference between a parameter and an argument? `[Basic]`

**Answer.** **Parameters** are the names in the definition. **Arguments** are the values at the call site.

```python
def f(x): ...   # x is a parameter
f(5)            # 5 is an argument
```

---

### Q61. What is the difference between `return` and `print()`? `[Basic]`

**Answer.** `print()` writes to stdout and returns `None`. `return` hands a value back to the caller and ends the function. Return-based functions compose and are testable; print-based functions are not.

```python
def add(a, b): return a + b
total = add(2, 3) * 10   # works

def show(a, b): print(a + b)
# show(2, 3) * 10        # TypeError: NoneType * int
```

---

### Q62. What does a function return without a `return` statement? `[Basic]`

**Answer.** `None`. A bare `return` also returns `None`.

---

### Q63. Can a function return multiple values? `[Intermediate]`

**Answer.** It returns **one tuple**, which the caller can unpack.

```python
def min_max(xs):
    return min(xs), max(xs)

low, high = min_max([3, 1, 2])
```

For clarity, return a dict or dataclass when fields need names.

---

### Q64. When is a function body executed? `[Intermediate]`

**Answer.** Not at `def` time. `def` compiles the body, evaluates defaults, and creates the function object. The body runs on each call. This is why defaults are evaluated once.

---

### Q65. Are functions objects? `[Intermediate]`

**Answer.** Yes — first-class. You can assign them, pass them, return them, and store them in data structures.

```python
ops = {"add": lambda a, b: a + b}
ops["add"](2, 3)   # 5
```

This is the foundation of callbacks, strategies, and decorators.

---

### Q66. Can you define a function inside a function? `[Intermediate]`

**Answer.** Yes. The inner function is local and can close over the outer function's variables (a closure). It is not visible outside the outer function.

---

### Q67. What is a docstring? `[Basic]`

**Answer.** The first string literal in a module/class/function, stored in `__doc__` and shown by `help()`/IDEs. It documents the **contract**: inputs, outputs, errors, and intent.

---

### Q68. How should functions be named and sized? `[Basic]`

**Answer.** `snake_case`, verb phrases (`calculate_tax`, `is_valid`), one responsibility, few parameters. If the name needs "and", split the function.

---

### Q69. What is a pure function? `[Intermediate]`

**Answer.** Same inputs → same output, with no side effects. Easy to test and reason about.

```python
def add_tax(amount, rate):   # pure
    return amount * (1 + rate)
```

---

### Q70. What is the call stack? `[Intermediate]`

**Answer.** The runtime structure tracking active function calls. Each call pushes a frame with local names and a return address; it pops on return. Tracebacks show this stack, which is why recursion can overflow it.

---

### Q71. What does `if __name__ == "__main__":` do? `[Intermediate]`

**Answer.** Runs the block only when the file is executed directly. When imported, `__name__` is the module name, so import-time side effects are avoided.

---

### Q72. Can functions be defined conditionally or dynamically? `[Advanced]`

**Answer.** Yes. `def` is an executable statement, so it can appear inside `if`, loops, or other functions. The name is bound when the statement runs.

```python
if os.name == "nt":
    def clear(): os.system("cls")
else:
    def clear(): os.system("clear")
```

---

# 5. Function Arguments

### Q73. Positional vs keyword arguments? `[Basic]`

**Answer.** Positional arguments match by **order**; keyword arguments match by **name**. Positional arguments must come before keyword arguments at the call site.

```python
def f(a, b): ...
f(1, 2)          # positional
f(b=2, a=1)      # keyword, order is free
```

---

### Q74. What happens if you pass too few or too many arguments? `[Basic]`

**Answer.** `TypeError`:

- missing required positional argument
- takes N positional arguments but M were given
- unexpected keyword argument
- got multiple values for argument

---

### Q75. When are default arguments evaluated? `[Intermediate]`

**Answer.** **Once**, when the `def` statement executes, and stored in `__defaults__`. They are not re-evaluated per call.

```python
def f(x, items=[]): ...
f.__defaults__   # ([],)
```

---

### Q76. Why is `def f(x, items=[])` dangerous? `[Trap]`

**Answer.** The **same list** is reused across calls, so state leaks.

```python
def f(x, items=[]):
    items.append(x)
    return items

f(1)   # [1]
f(2)   # [1, 2]  <- bug
```

**Fix:**

```python
def f(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items
```

---

### Q77. What if `None` is a valid input? `[Advanced]`

**Answer.** Use a unique sentinel:

```python
SENTINEL = object()

def f(x, items=SENTINEL):
    if items is SENTINEL:
        items = []
    ...
```

For dataclasses, use `field(default_factory=list)`.

---

### Q78. What is `*args`? `[Basic]`

**Answer.** Collects extra **positional** arguments into a **tuple**. The name `args` is conventional; `*values` works too.

```python
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)      # 6
total(*[1, 2, 3])   # 6 (unpacking)
```

---

### Q79. What is `**kwargs`? `[Basic]`

**Answer.** Collects extra **keyword** arguments into a **dict** with string keys.

```python
def profile(**fields):
    return fields

profile(name="Rohit", age=25)   # {'name': 'Rohit', 'age': 25}
```

---

### Q80. What is the parameter order in a signature? `[Advanced]`

**Answer.**

```text
def f(pos_only, /, normal, default=1, *args, kw_only, kw_default=2, **kwargs):
```

Order: positional-only → normal → `*args` → keyword-only → `**kwargs`.

---

### Q81. What does `/` mean in a signature? `[Advanced]`

**Answer.** Everything before it is **positional-only** (PEP 570). Passing those names as keywords raises `TypeError`. Useful when parameter names are implementation details or when `**kwargs` may contain the same key.

---

### Q82. What does a bare `*` mean in a signature? `[Advanced]`

**Answer.** Everything after it is **keyword-only**. Great for boolean flags:

```python
def create_user(name, *, active=True): ...
create_user("Rohit", active=False)   # readable
```

---

### Q83. What is argument unpacking? `[Intermediate]`

**Answer.** `*iterable` expands to positional arguments; `**mapping` expands to keyword arguments. Also works in literals.

```python
point(*[1, 2, 3])
point(**{"x": 1, "y": 2, "z": 3})
[*a, *b]
{**d1, **d2}
```

---

### Q84. How do you forward arguments in a wrapper? `[Advanced]`

**Answer.**

```python
def wrapper(*args, **kwargs):
    return target(*args, **kwargs)
```

This preserves any signature and is the basis of decorators.

---

### Q85. Are arguments passed by value or by reference? `[Advanced]`

**Answer.** Neither exactly — Python uses **call by object reference (call by sharing)**. The function receives references to the same objects. Rebinding a parameter inside the function does not affect the caller; mutating a mutable object does.

```python
def rebind(x):
    x = 99          # local rebinding, caller unchanged

def mutate(xs):
    xs.append(99)   # caller's list changes
```

---

### Q86. Can a default value reference another parameter? `[Trap]`

**Answer.** No. Defaults are evaluated at definition time in the enclosing scope:

```python
def f(a, b=a):   # NameError
    ...
```

---

### Q87. Can you pass the same parameter twice? `[Basic]`

**Answer.** No: `f(1, a=2)` raises `TypeError: got multiple values for argument 'a'`. The same applies when an explicit keyword collides with `**` unpacking.

---

### Q88. How do you merge dictionaries with `**`? `[Intermediate]`

**Answer.**

```python
merged = {**defaults, **overrides}
```

Later keys win. This is a shallow merge, not a deep merge.

---

### Q89. What are the trade-offs of `**kwargs`? `[Advanced]`

**Answer.** Flexible and useful for forwarding/configuration, but it hides the API, weakens editor support and type checking, and can silently accept typos. Prefer explicit parameters; use `**kwargs` when forwarding or when the set of options is genuinely open.

---

# 6. Scope, LEGB, Closures

### Q90. Explain the LEGB rule. `[Basic]`

**Answer.** Name lookup order:

1. **L**ocal — current function
2. **E**nclosing — outer functions
3. **G**lobal — module
4. **B**uilt-in — `len`, `print`, ...

First match wins; otherwise `NameError`. Scope is **lexical/static**, decided at compile time.

---

### Q91. Is a variable local if it is assigned anywhere in the function? `[Trap]`

**Answer.** Yes. The compiler marks it local for the **whole** function, even before the assignment runs. Reading it first raises `UnboundLocalError`.

```python
x = 1
def f():
    print(x)   # UnboundLocalError
    x = 2
```

---

### Q92. Do you need `global` to read a global? `[Basic]`

**Answer.** No. Only to **rebind** it. Reading resolves through LEGB.

---

### Q93. When do you need `global`? `[Intermediate]`

**Answer.** When assigning/rebinding a module-level name inside a function, including augmented assignment (`x += 1`).

```python
count = 0
def increment():
    global count
    count += 1
```

---

### Q94. Do you need `global` to mutate a global list? `[Trap]`

**Answer.** No. `items.append(x)` mutates the object; it does not rebind the name. You need `global` only for `items = [...]`.

---

### Q95. What is `nonlocal`? `[Intermediate]`

**Answer.** Declares that a name refers to the nearest **enclosing function** scope, enabling rebinding. It does not reach module globals.

```python
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
```

---

### Q96. Difference between `global` and `nonlocal`? `[Basic]`

**Answer.** `global` targets the module scope; `nonlocal` targets the nearest enclosing function scope. Both are needed only for rebinding. `nonlocal` at module level is a `SyntaxError`.

---

### Q97. What is a closure? `[Intermediate]`

**Answer.** A nested function that retains references to names from its enclosing scope after that scope returns. It is how counters and decorators keep state.

```python
def make_multiplier(k):
    return lambda x: x * k
```

---

### Q98. Why do lambdas in a loop all return the last value? `[Trap]`

**Answer.** Closures capture **variables**, not values (late binding). At call time the loop variable holds its final value.

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]   # [2, 2, 2]
```

Fixes: `lambda i=i: i` or a factory function.

---

### Q99. Does a comprehension leak its loop variable? `[Intermediate]`

**Answer.** No in Python 3 — comprehensions have their own scope. (Python 2 list comprehensions did leak.)

---

### Q100. Can a comprehension inside a class body see class attributes? `[Advanced]`

**Answer.** No. The comprehension's enclosing scope skips the class body, so a bare class attribute name raises `NameError`. Compute it in a method/`__init__`, or reference `self`.

---

### Q101. What happens if you shadow a built-in? `[Intermediate]`

**Answer.** The module-level name hides the built-in for that scope.

```python
len = 5
len("abc")   # TypeError: 'int' object is not callable
del len      # built-in visible again
```

Avoid names such as `list`, `dict`, `str`, `sum`, `min`, `max`, `id`, `type`, `input`.

---

### Q102. Is Python scope lexical or dynamic? `[Advanced]`

**Answer.** Lexical (static). A function uses the scope where it was **defined**, not where it is called. This is why closures work and why moving code between modules can change visible globals.

---

### Q103. What are `globals()` and `locals()`? `[Advanced]`

**Answer.** `globals()` returns the module namespace dict; `locals()` returns a snapshot-like dict of the current local namespace. They are diagnostic tools, not design tools; modifying `locals()` is not guaranteed to affect real locals.

---

### Q104. Why avoid global state? `[Intermediate]`

**Answer.** Hidden coupling, harder testing, action at a distance, order-dependent bugs, and concurrency issues. Pass dependencies in and return results. Module-level **constants** are fine; mutable globals are the problem.

---

# 7. Lambda, map, filter, sorted, Documentation, Typing

### Q105. What is a lambda? `[Basic]`

**Answer.** An anonymous function containing a **single expression**. The expression's value is returned automatically.

```python
square = lambda x: x * x
square(5)   # 25
```

---

### Q106. What can a lambda NOT do? `[Intermediate]`

**Answer.** No statements, assignments, `return`, annotations, or docstrings. Only one expression.

---

### Q107. lambda vs `def`? `[Basic]`

**Answer.** `lambda` is compact and anonymous, ideal as a key/callback. `def` is named, multi-statement, documentable, testable, and appears properly in tracebacks. PEP 8 says do not assign a lambda to a name — use `def`.

---

### Q108. What is a higher-order function? `[Intermediate]`

**Answer.** A function that takes another function as an argument or returns one. Examples: `map`, `filter`, `sorted`, decorators, factories.

---

### Q109. What does `map()` return in Python 3? `[Basic]`

**Answer.** A **lazy iterator**, not a list. Consume it with `list()`, `tuple()`, `sum()`, etc. It is exhausted after one pass. With multiple iterables it stops at the shortest.

---

### Q110. `map()` vs a list comprehension? `[Intermediate]`

**Answer.** Both transform. Comprehensions are usually more readable for expressions/filters; `map()` is concise when a function already exists (`map(str, xs)`). In Python 3, `map` is lazy.

---

### Q111. What does `filter()` do? `[Basic]`

**Answer.** Keeps items whose predicate is truthy, returning a lazy iterator. `filter(None, iterable)` keeps truthy items (drops `0`, `""`, `None`, `[]`, `False`).

---

### Q112. How does `sorted(key=...)` work? `[Intermediate]`

**Answer.** `key` is called **once per element**; sorting compares the returned keys. It is stable and O(n log n), and returns a new list.

```python
sorted(words, key=str.casefold)
sorted(students, key=lambda s: s[1], reverse=True)
```

---

### Q113. How do you sort by multiple fields? `[Intermediate]`

**Answer.** Return a tuple. Use negation for descending numeric fields.

```python
sorted(students, key=lambda s: (-s.score, s.name))
```

---

### Q114. What does "stable sort" mean? `[Advanced]`

**Answer.** Elements with equal keys keep their original relative order. Python's `sorted`/`list.sort` are stable (Timsort), which enables multi-pass sorting tricks.

---

### Q115. `sort()` vs `sorted()`? `[Basic]`

**Answer.** `list.sort()` is in-place and returns `None`; `sorted()` returns a new list and accepts any iterable.

---

### Q116. What are `itemgetter` and `attrgetter`? `[Advanced]`

**Answer.** `operator` helpers that build fast key functions for subscripts/attributes:

```python
sorted(rows, key=itemgetter(1))
sorted(people, key=attrgetter("score"))
```

Often faster and clearer than a lambda for simple field access.

---

### Q117. How do `any()` and `all()` behave on empty iterables? `[Trap]`

**Answer.** `all([])` is `True` (vacuous truth); `any([])` is `False`. Both short-circuit.

---

### Q118. What is `reduce()`? `[Advanced]`

**Answer.** `functools.reduce(func, iterable, initial)` folds left to right into one value.

```python
reduce(lambda acc, x: acc + x, [1, 2, 3], 0)   # 6
```

`sum`, `min`, `max`, and `math.prod` are clearer for common cases.

---

### Q119. What is `functools.partial`? `[Advanced]`

**Answer.** Freezes some arguments and returns a new callable.

```python
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
square(9)   # 81
```

Useful for callbacks and configuration.

---

### Q120. What belongs in a docstring? `[Intermediate]`

**Answer.** Summary line, then inputs, outputs, raised exceptions, side effects, and important assumptions. Google/NumPy/Sphinx styles are common. Document the **contract**, not the syntax.

---

### Q121. Are type hints enforced at runtime? `[Trap]`

**Answer.** No. They are metadata stored in `__annotations__`, used by editors, mypy/pyright, and frameworks. Runtime validation requires pydantic or explicit checks.

```python
def f(x: int) -> str: ...
f("not an int")   # runs fine
```

---

### Q122. Show common type hints. `[Intermediate]`

**Answer.**

```python
def f(items: list[int], mapping: dict[str, int]) -> tuple[int, ...]: ...
def g(name: str | None = None) -> str: ...
from typing import Callable, Any
def h(func: Callable[[int], int], value: int) -> int: ...
```

`str | None` needs 3.10+; older code uses `Optional[str]`.

---

### Q123. Why use type hints? `[Intermediate]`

**Answer.** Editor completion, refactoring safety, static bug detection, documentation, and API schema generation (FastAPI/pydantic). They do not replace tests.

---

### Q124. What is `from __future__ import annotations`? `[Advanced]`

**Answer.** Postpones annotation evaluation, storing them as strings. It helps with forward references and import cycles. Python 3.14 uses lazy annotations by default (PEP 649), reducing the need.

---

# 8. Function Design & Side Effects

### Q125. What makes a good function? `[Basic]`

**Answer.** One responsibility, a verb name, explicit inputs/outputs, validation at the boundary, no hidden globals, documented side effects, and testability.

---

### Q126. What is a side effect? `[Intermediate]`

**Answer.** Any observable interaction beyond returning a value: printing, mutating arguments/globals, file/network I/O, randomness, time. Necessary at the edges; dangerous when hidden in core logic.

---

### Q127. Pure vs impure functions? `[Intermediate]`

**Answer.** Pure: same inputs → same output, no side effects. Impure: depends on or changes external state. Keep calculation pure; push I/O to the edges.

---

### Q128. How do you avoid hidden state? `[Intermediate]`

**Answer.** Pass dependencies as parameters, return results, avoid mutable globals, document mutations, and prefer creating new objects over mutating inputs.

---

### Q129. Why is a function that only prints hard to reuse? `[Basic]`

**Answer.** Its result cannot be captured or composed; it also makes tests depend on captured stdout. Return the value and let the caller decide how to display it.

---

### Q130. How do you validate inputs? `[Intermediate]`

**Answer.** Fail fast at the boundary with clear errors: type checks, range checks, required keys, and explicit exceptions. Keep validation separate from computation so both are testable.

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount
```

---

### Q131. How do you make code testable? `[Intermediate]`

**Answer.** Small pure functions, dependency injection (pass clients/config), no hidden I/O, deterministic behaviour, and clear return values. Tests then need no network/database.

---

### Q132. How would you structure a text analyser? `[Intermediate]`

**Answer.** Separate layers:

1. Cleaning/tokenisation (`normalize_whitespace`, `tokenize`)
2. Pure analysis (`count_words`, `word_frequencies`, `count_sentences`)
3. Reporting (`build_report` returns a string)
4. I/O (`main` reads input and prints)

Document assumptions about words/sentences/characters.

---

### Q133. What is the mutable-default rule? `[Basic]`

**Answer.** Never use a mutable default (`[]`, `{}`, `set()`); use `None` or a sentinel and create a fresh object inside the function.

---

### Q134. How do you handle errors in a reusable function? `[Intermediate]`

**Answer.** Raise specific exceptions with actionable messages; do not print and continue silently. Let callers decide whether to recover. Avoid bare `except:`.

---

# 9. Recursion

### Q135. What is recursion? `[Basic]`

**Answer.** A function that calls itself on a smaller input. It needs a **base case** and a **recursive case** that moves toward the base case.

---

### Q136. What happens without a base case? `[Basic]`

**Answer.** Infinite recursion until `RecursionError: maximum recursion depth exceeded` (default limit ~1000).

---

### Q137. Trace `factorial(4)`. `[Intermediate]`

**Answer.**

```text
factorial(4) = 4 * factorial(3)
             = 4 * 3 * factorial(2)
             = 4 * 3 * 2 * factorial(1)
             = 4 * 3 * 2 * 1
             = 24
```

Each pending call holds a stack frame.

---

### Q138. Does Python optimise tail recursion? `[Advanced]`

**Answer.** No. Even a tail call adds a frame. Use iteration for deep/unbounded loops, or increase the limit deliberately (with care).

---

### Q139. Why is naive Fibonacci slow? `[Advanced]`

**Answer.** It recomputes the same subproblems exponentially — O(2ⁿ). Memoise with `functools.lru_cache` → O(n), or use the iterative O(n) time / O(1) space version.

---

### Q140. Recursion vs iteration? `[Intermediate]`

**Answer.** Recursion is expressive for trees, divide-and-conquer, and backtracking. Iteration is safer for deep/linear repetition and usually more memory-efficient. Python's lack of tail-call optimisation matters.

---

### Q141. How do you flatten a nested list recursively? `[Advanced]`

**Answer.**

```python
def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

---

### Q142. How do you check a palindrome recursively? `[Advanced]`

**Answer.** Clean the text, then compare the ends and recurse inward:

```python
def is_palindrome(text):
    chars = [c.casefold() for c in text if c.isalnum()]
    def check(lo, hi):
        if lo >= hi:
            return True
        if chars[lo] != chars[hi]:
            return False
        return check(lo + 1, hi - 1)
    return check(0, len(chars) - 1)
```

---

### Q143. What is memoisation? `[Intermediate]`

**Answer.** Caching results of expensive calls keyed by arguments. `functools.lru_cache` is the standard tool for pure functions with hashable arguments.

---

### Q144. When should you avoid recursion? `[Intermediate]`

**Answer.** When depth can be large or unbounded, when the recursive step copies data unnecessarily, or when a simple loop is clearer. Python's stack limit and per-call overhead favour iteration in those cases.

---

# 10. Output Prediction Drills

Cover the answer, predict, then check.

### D1.

```python
s = "Python"
print(s[-1], s[:2], s[2:], s[::-1])
```

**Output:** `n Py thon nohtyP`

---

### D2.

```python
print(repr("abc"[10:20]), len("abc"[10:20]))
```

**Output:** `'' 0` — slices clamp; they never raise `IndexError`.

---

### D3.

```python
print("5" + "5", "5" * 3)
```

**Output:** `55 555`

---

### D4.

```python
print("10" < "9", int("10") < int("9"))
```

**Output:** `True False` — string comparison is lexicographic.

---

### D5.

```python
print("Z" < "a", "apple" < "app")
```

**Output:** `True False` — `"app"` is a prefix, so it is smaller.

---

### D6.

```python
print("banana".count("a"), "aaa".count("aa"))
```

**Output:** `3 1` — `count` is non-overlapping.

---

### D7.

```python
print(" a  b ".split(), " a  b ".split(" "))
```

**Output:** `['a', 'b'] ['', 'a', '', 'b', '']`

---

### D8.

```python
print("-".join("abc"))
```

**Output:** `a-b-c` — `join` accepts any iterable of strings, including a string.

---

### D9.

```python
print("Hello".replace("l", "L", 2))
```

**Output:** `HeLLo` — only the first two matches.

---

### D10.

```python
print("  x  ".strip(), "xxhixx".strip("x"))
```

**Output:** `x hi`

---

### D11.

```python
print(f"{3.14159:.2f}", f"{42:05d}", f"{'x':^5}.")
```

**Output:** `3.14 00042   x  .`

---

### D12.

```python
def f(a, b=[]):
    b.append(a)
    return b

print(f(1))
print(f(2))
```

**Output:**

```text
[1]
[1, 2]
```

The default list is shared.

---

### D13.

```python
def f(x):
    print(x)

print(f(1))
```

**Output:**

```text
1
None
```

`print` returns `None`, which the outer `print` displays.

---

### D14.

```python
x = 10
def f():
    x = 20
    return x
print(f(), x)
```

**Output:** `20 10` — the assignment creates a local.

---

### D15.

```python
x = 10
def f():
    print(x)
    x = 20
f()
```

**Output:** `UnboundLocalError` — `x` is local for the whole function.

---

### D16.

```python
def f(*args, **kwargs):
    return len(args), len(kwargs)
print(f(1, 2, a=3))
```

**Output:** `(2, 1)`

---

### D17.

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
```

**Output:** `[2, 2, 2]` — late binding.

---

### D18.

```python
print(sorted(["bb", "a", "ccc"], key=len))
```

**Output:** `['a', 'bb', 'ccc']`

---

### D19.

```python
print(list(map(lambda x: x * 2, [1, 2, 3])))
print(list(filter(lambda x: x > 1, [1, 2, 3])))
```

**Output:**

```text
[2, 4, 6]
[2, 3]
```

---

### D20.

```python
def f(a, b=2, *args, c=3):
    return a, b, args, c
print(f(1, 4, 5, 6))
```

**Output:** `(1, 4, (5, 6), 3)`

---

### D21.

```python
print(bool(""), bool(" "), bool("0"))
```

**Output:** `False True True` — only the empty string is falsy.

---

### D22.

```python
print("abc".startswith(("x", "a")), "abc".endswith("bc"))
```

**Output:** `True True`

---

# 11. Debugging & Code Review Drills

### B1. Fix the mutation error.

```python
s = "hello"
s[0] = "H"
```

**Fix:** `s = "H" + s[1:]` or `s = "H" + s[1:]`. Strings are immutable.

---

### B2. Fix the type error.

```python
print("Age: " + 25)
```

**Fix:** `print(f"Age: {25}")` or `print("Age: " + str(25))`.

---

### B3. The developer expected `report` but got `repor`.

```python
name = "report.txt"
print(name.strip(".txt"))   # 'repor'
```

**Why:** `strip` treats its argument as a **character set**, so it also removes the trailing `t` of `report`. **Fix:** `name.removesuffix(".txt")`.

---

### B4. Why does this leak state?

```python
def add(value, items=[]):
    items.append(value)
    return items
```

**Fix:** `items=None` + create a new list inside. Explain that defaults are evaluated once at definition time.

---

### B5. Why does `total` fail?

```python
total = 0
def add(n):
    total += n
```

**Fix:** declare `global total` (or, better, return a new total and avoid global state).

---

### B6. Why is the result always `None`?

```python
def double(x):
    x * 2

result = double(5)
```

**Fix:** `return x * 2`. The function computes and discards the value.

---

### B7. Why do all callbacks print `2`?

```python
callbacks = [lambda: i for i in range(3)]
```

**Fix:** `lambda i=i: i` or a factory function. Closures capture variables, not values.

---

### B8. Why does `join` fail?

```python
",".join([1, 2, 3])
```

**Fix:** `",".join(map(str, [1, 2, 3]))`.

---

### B9. Why does this sort incorrectly?

```python
sorted(words, key=words.lower())
```

**Why:** the key is called with no arguments and `words` is a list. **Fix:** `sorted(words, key=str.lower)`.

---

### B10. Why is the type hint not preventing bad input?

```python
def f(x: int) -> int:
    return x * 2

f("a")
```

**Answer:** Type hints are not enforced at runtime. Use validation or a checker.

---

### B11. Why does recursion crash?

```python
def countdown(n):
    print(n)
    countdown(n - 1)
```

**Fix:** add a base case (`if n == 0: return`).

---

### B12. Why is the output order surprising?

```python
def f():
    print("body")

print("before")
f()
print("after")
```

**Answer:** `def` does not run the body. Output is `before`, `body`, `after`; the body runs at the call.

---

# 12. Coding Challenges with Solutions

> In an interview, state assumptions first, then write the smallest correct function, then discuss edge cases and complexity.

### C1. Reverse a string without slicing. `[Basic]`

```python
def reverse(text: str) -> str:
    chars = list(text)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)
```

**Complexity:** O(n) time, O(n) space.

---

### C2. Palindrome check ignoring case, spaces, punctuation. `[Basic]`

```python
def is_palindrome(text: str) -> bool:
    chars = [c.casefold() for c in text if c.isalnum()]
    return chars == chars[::-1]
```

**Follow-up:** do it with two pointers and O(1) extra space.

---

### C3. Count vowels and consonants. `[Basic]`

```python
def count_vowels_consonants(text: str) -> tuple[int, int]:
    vowels = consonants = 0
    for ch in text.casefold():
        if ch in "aeiou":
            vowels += 1
        elif ch.isalpha():
            consonants += 1
    return vowels, consonants
```

**Assumption:** `y` is a consonant; non-letters ignored.

---

### C4. Anagram check. `[Basic]`

```python
from collections import Counter

def are_anagrams(a: str, b: str) -> bool:
    def clean(text: str):
        return Counter(c.casefold() for c in text if c.isalnum())
    return clean(a) == clean(b)
```

**Complexity:** O(n) average. Alternative: sorted strings, O(n log n).

---

### C5. First non-repeating character. `[Intermediate]`

```python
from collections import Counter

def first_unique(text: str) -> str | None:
    counts = Counter(text)
    for ch in text:
        if counts[ch] == 1:
            return ch
    return None
```

**Follow-up:** return its index. **Trap:** do not sort; order matters.

---

### C6. Run-length encoding and decoding. `[Intermediate]`

```python
def encode(text: str) -> str:
    if not text:
        return ""
    parts = []
    prev, count = text[0], 1
    for ch in text[1:]:
        if ch == prev:
            count += 1
        else:
            parts.append(f"{prev}{count}")
            prev, count = ch, 1
    parts.append(f"{prev}{count}")
    return "".join(parts)

def decode(code: str) -> str:
    result = []
    i = 0
    while i < len(code):
        ch = code[i]
        i += 1
        digits = []
        while i < len(code) and code[i].isdigit():
            digits.append(code[i])
            i += 1
        result.append(ch * int("".join(digits) or 1))
    return "".join(result)
```

**Trap:** multi-digit counts; empty input; decoding invalid input.

---

### C7. Caesar cipher. `[Intermediate]`

```python
def caesar(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)
```

**Discussion:** `str.isalpha()` accepts non-ASCII letters; `ord` arithmetic then breaks. For ASCII-only, check `ch.isascii() and ch.isalpha()`.

---

### C8. Longest common prefix. `[Intermediate]`

```python
def longest_common_prefix(words: list[str]) -> str:
    if not words:
        return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
```

**Complexity:** O(total characters) worst case.

---

### C9. String rotation check. `[Intermediate]`

```python
def is_rotation(a: str, b: str) -> bool:
    return len(a) == len(b) and a in b + b
```

**Explain:** every rotation of `a` appears inside `b + b`. Check lengths to avoid false positives.

---

### C10. Title-case without `title()`. `[Basic]`

```python
def title_case(text: str) -> str:
    return " ".join(
        word[:1].upper() + word[1:].lower()
        for word in text.split()
    )
```

---

### C11. Remove duplicate characters preserving order. `[Basic]`

```python
def unique_chars(text: str) -> str:
    seen = set()
    out = []
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)
```

**Follow-up:** `"".join(dict.fromkeys(text))` does the same in one line (dicts preserve insertion order in 3.7+).

---

### C12. Word frequency excluding stop words. `[Intermediate]`

```python
from collections import Counter

STOP_WORDS = {"the", "a", "an", "is", "and", "of", "to", "in"}

def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    words = [w.strip(".,!?;:").casefold() for w in text.split()]
    words = [w for w in words if w and w not in STOP_WORDS]
    counts = Counter(words)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
```

**Trap:** punctuation and case must be normalised first; ties need a deterministic rule.

---

### C13. Flatten an arbitrarily nested list. `[Intermediate]`

```python
def flatten(items: list) -> list:
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

**Follow-up:** use an explicit stack to avoid recursion depth limits.

---

### C14. Factorial and Fibonacci (recursive + memoised). `[Intermediate]`

```python
from functools import lru_cache

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    return 1 if n < 2 else n * factorial(n - 1)

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

**Discuss:** naive Fibonacci is O(2ⁿ); memoised is O(n); iterative is O(1) space.

---

### C15. Validate a simple email address. `[Intermediate]`

```python
def is_valid_email(email: str) -> bool:
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return "." in domain and " " not in email
```

**Important:** this is a heuristic, not RFC 5322. In production, validate with a library or send a confirmation email.

---

### C16. Collapse extra whitespace. `[Basic]`

```python
def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())
```

**Explain:** `split()` with no arguments already treats runs of whitespace as one separator.

---

### C17. Count sentences with assumptions. `[Intermediate]`

```python
import re

def count_sentences(text: str) -> int:
    if not text.strip():
        return 0
    parts = re.split(r"[.!?]+", text)
    return sum(1 for part in parts if part.strip())
```

**Say:** "This treats runs of terminators as one boundary and counts trailing text without a terminator. It does not handle abbreviations."

---

### C18. Implement `zip`-like pairing without `zip`. `[Advanced]`

```python
def pairs(a: list, b: list) -> list[tuple]:
    return [(a[i], b[i]) for i in range(min(len(a), len(b)))]
```

**Follow-up:** explain why `zip` is lazy in Python 3 and stops at the shortest iterable.

---

### C19. Design a reusable `summarize_text` API. `[Advanced]`

```python
def summarize_text(text: str) -> dict[str, object]:
    words = text.split()
    return {
        "characters": len(text),
        "words": len(words),
        "unique_words": len({w.casefold() for w in words}),
        "longest_word": max(words, key=len, default=""),
    }
```

**Discuss:** return data, not prose; let the caller format it. Document assumptions and handle empty input (`default=""`).

---

# 13. Rapid-Fire One-Liners

| # | Question | Answer |
|---:|---|---|
| 1 | Reverse a string | `s[::-1]` |
| 2 | Last character | `s[-1]` |
| 3 | First three characters | `s[:3]` |
| 4 | Remove leading/trailing spaces | `s.strip()` |
| 5 | Remove a known suffix | `s.removesuffix(suffix)` |
| 6 | Split a CSV line | `line.split(",")` |
| 7 | Split on any whitespace | `text.split()` |
| 8 | Join words | `" ".join(words)` |
| 9 | Find a substring safely | `s.find(sub)` → `-1` if absent |
| 10 | Find or raise | `s.index(sub)` |
| 11 | Count occurrences | `s.count(sub)` (non-overlapping) |
| 12 | Case-insensitive compare | `a.casefold() == b.casefold()` |
| 13 | Check prefix options | `s.startswith(("a", "b"))` |
| 14 | Reverse words in a sentence | `" ".join(s.split()[::-1])` |
| 15 | Remove all whitespace | `"".join(s.split())` |
| 16 | String to bytes | `s.encode("utf-8")` |
| 17 | Bytes to string | `b.decode("utf-8")` |
| 18 | Length in bytes | `len(s.encode("utf-8"))` |
| 19 | Format 2 decimals | `f"{x:.2f}"` |
| 20 | Pad an integer | `f"{n:05d}"` |
| 21 | Default return value | `None` |
| 22 | Multiple return values | A tuple; unpack it |
| 23 | Mutable default fix | `None` + create inside |
| 24 | `*args` type | `tuple` |
| 25 | `**kwargs` type | `dict` |
| 26 | Keyword-only marker | `*` |
| 27 | Positional-only marker | `/` |
| 28 | Name lookup order | LEGB |
| 29 | Rebinding a global | `global name` |
| 30 | Rebinding an enclosing variable | `nonlocal name` |
| 31 | Anonymous function | `lambda` |
| 32 | `map()` returns | Lazy iterator |
| 33 | `filter()` returns | Lazy iterator |
| 34 | Sort by a field | `sorted(items, key=itemgetter(1))` |
| 35 | Sort descending | `reverse=True` or negate numeric keys |
| 36 | Type hints enforced? | No, metadata only |
| 37 | Function docstring attribute | `__doc__` |
| 38 | Run only as a script | `if __name__ == "__main__":` |
| 39 | Recursion needs | Base case + progress |
| 40 | Infinite recursion error | `RecursionError` |

---

# 14. Behavioural & Communication Questions

### Q145. How would you explain string immutability to a junior? `[Basic]`

**Model:** "A string is like a printed label. You cannot edit the label in place; you print a new one and stick it over the old one. That is why every string method returns a new string."

---

### Q146. Tell me about a time you refactored a large function. `[Intermediate]`

**Structure:** situation → problem (responsibilities mixed, hard to test) → action (extracted pure functions, named steps, added tests) → result (smaller diff, faster tests, fewer regressions).

---

### Q147. How do you decide between recursion and iteration? `[Intermediate]`

**Model:** "I use recursion when the data is recursive — trees, nested JSON, divide-and-conquer — and iteration when the process is linear or depth can be large. Python has no tail-call optimisation, so deep recursion is a risk."

---

### Q148. How do you ensure a function is testable? `[Intermediate]`

**Model:** "I keep it pure where possible, pass dependencies in, return values instead of printing, and push I/O to the edges. Then tests are deterministic and fast."

---

### Q149. A reviewer says your function has a hidden side effect. How do you respond? `[Intermediate]`

**Model:** "I would confirm the behaviour, make the mutation explicit in the name/docstring, and prefer returning a new object. If mutation is required for performance, I would document it and add a test."

---

### Q150. How do you handle ambiguous requirements? `[Intermediate]`

**Model:** "I state assumptions explicitly, encode them in the function contract, and confirm with the stakeholder. For the text analyser, that means defining what counts as a word, sentence, and character."

---

### Q151. How do you debug an `UnboundLocalError`? `[Intermediate]`

**Model:** "I check whether the name is assigned anywhere in the function. If it is, Python treats it as local for the whole function. Then I decide whether I meant a local or needed `global`/`nonlocal`."

---

### Q152. Why should a function return instead of print? `[Basic]`

**Model:** "Returning makes the result usable by other code and testable without capturing stdout. Printing is a presentation decision that belongs to the caller."

---

# 15. 45-Minute Mock Interview Plan

| Time | Stage | What to practise |
|---:|---|---|
| 0–5 min | Warm-up | String basics, indexing, slicing, immutability |
| 5–12 min | Methods | `split`/`join`, `strip`, `replace`, `find` vs `index` |
| 12–18 min | Unicode | str vs bytes, encode/decode, normalisation |
| 18–26 min | Functions | parameters vs arguments, return vs print, `*args`/`**kwargs` |
| 26–32 min | Scope | LEGB, `global`/`nonlocal`, `UnboundLocalError` |
| 32–36 min | Functional | lambda, map/filter, sorted key |
| 36–42 min | Coding | palindrome / word frequency / flatten |
| 42–45 min | Review | Explain trade-offs and edge cases |

**Interviewer prompts to rehearse**

- "What happens if I pass a list as a default?"
- "Why does this raise `UnboundLocalError`?"
- "Can you rewrite that with a comprehension?"
- "What is the time complexity?"
- "How would you test this?"
- "What assumption did you make?"

---

# 16. Self-Scoring Rubric

Score each answer 0–3:

| Score | Meaning |
|---:|---|
| 0 | Could not answer |
| 1 | Partial / vague |
| 2 | Correct, but missing mechanism or example |
| 3 | Correct + mechanism + example + caveat |

**Target before the interview**

- All `[Basic]` questions: **3**
- All `[Intermediate]` questions: **2–3**
- `[Advanced]` questions: **2+** and improving
- Coding challenges: solve in **under 10 minutes** with edge cases stated

**Red flags to eliminate**

- Saying "string is a list of characters".
- Saying `is` compares strings safely.
- Forgetting that defaults are evaluated once.
- Claiming Python passes arguments by value or by reference without nuance.
- Forgetting that `print()` returns `None`.
- Claiming type hints are enforced.
- Writing recursion without a base case.

---

## One-Page Summary (Memorise This)

```text
STRING      immutable sequence of Unicode code points
INDEX       s[0], s[-1]; out of range -> IndexError
SLICE       s[start:stop:step]; clamped; new string; s[::-1] reverses
IMMUTABLE   any change -> new object; hashable -> dict keys
BUILD       "".join(parts), not += in a loop
COMPARE     == value, is identity; lexicographic by code point
ENCODING    str.encode("utf-8") / bytes.decode("utf-8")
FUNCTION    named callable object; first-class; returns None by default
RETURN      hands value back; print displays
DEFAULTS    evaluated once at def time -> never use []
ARGS        positional, keyword, *args tuple, **kwargs dict
MARKERS     / positional-only, * keyword-only
SCOPE       LEGB; global/nonlocal only for rebinding
CLOSURE     captures variables, not values -> lambda i=i fix
LAMBDA      one expression; use def for reusable logic
MAP/FILTER  lazy iterators in Python 3
SORTED      key called once per item; stable; tuple keys
TYPES       hints are metadata, not runtime enforcement
DESIGN      one responsibility; pure core; I/O at edges
RECURSION   base case + progress; no tail-call optimisation
```

> **Interview rule:** answer the question asked, name the mechanism, give one example, then stop. Depth beats breadth.
