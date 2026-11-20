"""
================================================================================
DAY 3 - INTERVIEW QUESTIONS (THEORY + PRACTICAL)
================================================================================

HOW TO USE THIS FILE
--------------------
1) Cover the answer, read only the question, and answer OUT LOUD.
2) Then read the model answer and compare structure, not just facts.
3) Run the practical section and predict each output BEFORE executing.

A strong interview answer has three parts:
  (1) the direct answer, (2) a one-line reason/mechanism, (3) an example.
================================================================================

==============================================================================
PART 1 - THEORY QUESTIONS
==============================================================================

--- STRINGS: FUNDAMENTALS ---

Q1. What exactly is a Python string?

A: An immutable sequence of Unicode code points. It supports indexing, slicing,
   len(), iteration, and membership because it implements the sequence protocol.
   There is no separate char type: s[0] returns a new 1-character str.
   Example: type("a"[0]) is str, len("a"[0]) == 1.

Q2. Why are strings immutable, and why is that useful?

A: The language guarantees the value cannot change after creation. This makes
   strings hashable (safe dict keys / set members), safe to share across
   functions and threads, and enables interning for fast equality.
   "Changing" a string always creates a new object and rebinds the name.

Q3. What is the difference between s[0] and s[0:1]?

A: Both produce a 1-character string. s[0] is an index lookup; s[0:1] is a
   slice and returns a new string. On a str the visible result is the same,
   but slicing is the general sequence operation and never raises IndexError.

Q4. What happens with out-of-range indexing vs out-of-range slicing?

A: Indexing raises IndexError. Slicing clamps the bounds and returns whatever
   is available (possibly ""), e.g. "abc"[10:20] == "".

Q5. How does negative indexing work?

A: -1 is the last element, -len(s) is the first. It is sugar for s[len(s) + i].
   Accessing below -len(s) raises IndexError.

Q6. How do you reverse a string?

A: s[::-1] is the idiomatic answer. Alternatives: "".join(reversed(s)).
   Note that reversal is by code point, so it can break grapheme clusters
   (combining accents, emoji ZWJ sequences).

Q7. What is the time complexity of string concatenation in a loop?

A: Each '+' copies both operands, so building a string with += in a loop is
   O(n^2) in the worst case. Collect parts in a list and use "".join(parts),
   which is O(n). (CPython has an in-place optimisation for += when the string's
   refcount is 1, but you must not rely on it.)

Q8. Difference between str and bytes?

A: str is Unicode text (code points). bytes is an immutable sequence of raw
   bytes (0-255). Convert with str.encode(encoding) and bytes.decode(encoding),
   normally UTF-8. Concatenating str and bytes raises TypeError.

Q9. Difference between UTF-8 and Unicode?

A: Unicode is the character set / code point standard. UTF-8 is one encoding
   of those code points into bytes (1-4 bytes per code point). Python str stores
   code points; encoding is only needed for I/O and storage.

Q10. Why is len("café") not always equal to len("café".encode("utf-8"))?

A: len(str) counts code points; len(bytes) counts bytes. In UTF-8, "é" takes
   2 bytes, so the str has length 4 and the bytes length 5. Also, a combining
   accent can make one visible character use 2 code points.

Q11. What are f-strings and why are they preferred?

A: Formatted string literals (3.6+): f"{name} is {age}". They are evaluated
   immediately, support expressions and a full format-spec mini-language, and
   are the fastest/readiest option for new code. Use .format() when the template
   is data, and %-style mainly for legacy code / lazy logging.

Q12. Difference between f-strings and %-formatting for logging?

A: f-strings are evaluated eagerly, even if the log level would discard the
   message. logging's %-style is lazy: logger.info("x=%s", x) formats only if
   the record is emitted. That is why logging prefers %-style.

--- STRINGS: METHODS ---

Q13. What is the difference between split() and split(" ")?

A: split() with no argument splits on runs of whitespace and drops empty
   strings. split(" ") splits on each single space and keeps empty strings.
   Example: " a  b ".split() -> ['a', 'b']; " a  b ".split(" ") ->
   ['', 'a', '', 'b', ''].

Q14. What does join() do, and what are its requirements?

A: "sep".join(iterable) concatenates strings with sep between them. Every item
   must be a str; otherwise TypeError. It is O(n) and preferred over +=.
   Common fix: ",".join(str(x) for x in numbers).

Q15. Difference between find() and index()?

A: Both search for a substring. find() returns -1 when absent; index() raises
   ValueError. Use find() when absence is expected, index() when it is a bug,
   and 'sub in text' when you only need a boolean.

Q16. Does count() count overlapping occurrences?

A: No. "aaa".count("aa") == 1. It scans left to right and skips past each
   found occurrence. count("") == len(s) + 1.

Q17. Difference between strip(), lstrip(), rstrip(), and replace()?

A: strip family removes characters from the ends only; with an argument it is a
   CHARACTER SET, not a prefix. replace() replaces substrings anywhere.
   To remove a known prefix/suffix use removeprefix()/removesuffix() (3.9+).

Q18. Difference between lower() and casefold()?

A: lower() is simple lowercasing for display. casefold() is aggressive
   Unicode caseless matching (e.g. "ß" folds to "ss"). Use casefold() when
   comparing case-insensitively.

Q19. What does startswith() accept besides a string?

A: A tuple of prefixes, e.g. name.startswith(("img_", "photo_")). Same for
   endswith(). Optional start/end arguments follow slice semantics.

Q20. What does title() do, and what is its gotcha?

A: It title-cases each word (first letter upper, rest lower), where words are
   separated by non-letters. "it's".title() -> "It'S" because the apostrophe is
   a boundary. For display names, a custom word splitter is safer.

Q21. Are string methods in-place?

A: No. str is immutable, so every method returns a new string (or list/int).
   The original is unchanged. This is a common "spot the bug" question.

Q22. How do you check if a string contains only digits?

A: s.isdigit() for a quick check, but note Unicode digits such as "²" pass
   isdigit() yet int("²") fails. s.isdecimal() is the safer pre-check before
   int(); alternatively try/except ValueError, which is the most robust.

Q23. How do you remove all whitespace from a string?

A: "".join(s.split()) collapses and removes whitespace. s.replace(" ", "")
   only removes spaces, not tabs/newlines. For only the ends, use strip().

Q24. How do you count words in a sentence?

A: len(text.split()) under the assumption "word = whitespace-separated token".
   For real text, strip punctuation and define edge cases (hyphens, apostrophes).

--- STRINGS: OTHER CONCEPTS ---

Q25. What does 'in' do for strings?

A: Substring membership, case-sensitive, no word boundaries: "ana" in
   "banana" is True. It is not a word check; tokenise first if you need words.

Q26. What is a raw string? Does it change the runtime type?

A: r"..." tells the parser not to interpret backslash escapes; the value keeps
   literal backslashes. It is still a str at runtime. It cannot end with an odd
   number of backslashes. Common for regex and Windows paths.

Q27. How are strings compared?

A: Lexicographically by Unicode code point. The first differing character
   decides; a prefix is smaller than the longer string. Uppercase sorts before
   lowercase ("Z" < "a"), and numeric strings do not compare numerically
   ("10" < "9" is True). Use casefold() for caseless comparison and int() for
   numeric comparison.

Q28. Difference between == and is for strings?

A: == compares values; is compares object identity. CPython interns some
   strings, so x is y may be True by accident. Always use == for values; use is
   only for None/True/False/sentinels.

Q29. What is Unicode normalisation and why does it matter?

A: Visually identical text can have different code-point sequences (composed
   "é" vs "e" + combining accent). Normalise with unicodedata.normalize("NFC",
   s) before comparing or storing user input.

Q30. Why can len() differ from the number of visible characters?

A: len() counts code points. Combining marks and emoji ZWJ sequences use
   multiple code points for one grapheme cluster.

--- FUNCTIONS: FUNDAMENTALS ---

Q31. What is a function, and why use one?

A: A named, callable object encapsulating behaviour, with parameters, a body,
   and an optional return value. It provides abstraction, reuse, testability,
   and local scope.

Q32. Parameter vs argument?

A: Parameters are the names in the definition; arguments are the values at the
   call site. "def f(x)" has parameter x; "f(5)" passes argument 5.

Q33. return vs print()?

A: print() writes to stdout and returns None. return hands a value back to the
   caller and ends the function. Return-based functions compose and are testable.

Q34. What does a function return without a return statement?

A: None.

Q35. Can a function return multiple values?

A: It returns one tuple; the caller can unpack it: a, b = f(). A dict or
   dataclass is clearer when fields need names.

Q36. When is a function body executed?

A: Not at def time. def compiles the body, evaluates defaults, and creates the
   function object. The body runs on each call.

Q37. Are functions first-class objects?

A: Yes: assign them, pass them, return them, store them in dicts/lists. This
   enables callbacks, strategies, map/filter, and decorators.

Q38. What is a pure function?

A: Same inputs -> same output, no side effects. Easy to test and reason about.
   Impure functions are fine at the I/O edges but should not hide state changes.

--- FUNCTIONS: ARGUMENTS ---

Q39. Positional vs keyword arguments?

A: Positional match by order; keyword match by name. Positional arguments must
   come before keyword arguments at the call site.

Q40. When are default arguments evaluated?

A: Once, when the def statement executes, and stored in __defaults__. This is
   why mutable defaults are shared across calls.

Q41. Why is def f(x, items=[]) dangerous? How do you fix it?

A: The same list is created once and reused, so calls leak state into each
   other. Fix: items=None, then create a new list inside when None.
   Proof: f.__defaults__ shows the mutated default.

Q42. *args vs **kwargs?

A: *args collects extra positional arguments into a tuple; **kwargs collects
   extra keyword arguments into a dict with string keys.

Q43. How do you forward arguments in a wrapper?

A: def wrapper(*args, **kwargs): return target(*args, **kwargs). This preserves
   any signature and is the basis of decorators.

Q44. What does a bare * mean in a signature? What does / mean?

A: Bare * marks all following parameters keyword-only. / marks all preceding
   parameters positional-only (PEP 570). They let you control the public API.

Q45. What is argument unpacking?

A: *iterable expands to positional arguments; **mapping expands to keyword
   arguments at the call site. Also works in literals: [*a, *b], {**d1, **d2}.

Q46. What errors occur for wrong argument counts?

A: Missing required -> TypeError "missing required positional argument".
   Extra positional -> TypeError "takes N positional arguments but M given".
   Unknown keyword -> TypeError "unexpected keyword argument".
   Duplicate value -> TypeError "got multiple values for argument".

--- SCOPE ---

Q47. Explain the LEGB rule.

A: Name resolution order: Local -> Enclosing -> Global -> Built-in. Python uses
   the first binding found; otherwise NameError. Scope is lexical/static.

Q48. global vs nonlocal?

A: global rebinds a module-level name; nonlocal rebinds the nearest enclosing
   function name. Both are needed only for REBINDING; reading works without them.

Q49. Why does this raise UnboundLocalError?
       x = 1
       def f():
           print(x)
           x = 2

A: The assignment makes x local for the whole function (decided at compile
   time). print(x) runs before the local is bound. Fix: global x, or remove the
   assignment, or assign before reading.

Q50. Do you need global to mutate a global list?

A: No. append() mutates the object without rebinding the name. You need global
   only to assign a new object to the name.

Q51. Does a comprehension leak its loop variable?

A: No in Python 3 - comprehensions have their own scope. In Python 2, list
   comprehensions leaked.

Q52. Why do lambdas in a loop all return the last value?

A: Closures capture variables, not values (late binding). At call time the loop
   variable holds its final value. Bind with a default (lambda i=i: i) or a
   factory function.

Q53. What is a closure?

A: A nested function that keeps references to names from its enclosing scope
   after that scope returns. It is how counters and decorators retain state.

--- FUNCTIONAL TOOLS / DOCS ---

Q54. lambda vs def?

A: lambda is an anonymous, single-expression function; no statements, no
   annotations, no docstring. Use def for anything reused or non-trivial.

Q55. What do map() and filter() return in Python 3?

A: Lazy iterators. Consume with list()/sum()/tuple(). They are exhausted after
   one pass. map stops at the shortest iterable when given several.

Q56. How does sorted(key=...) work?

A: key is called once per element; sorting compares the returned keys. It is
   stable, O(n log n), and returns a new list. For multiple criteria return a
   tuple; negate numeric fields for descending order.

Q57. sort() vs sorted()?

A: list.sort() is in-place and returns None. sorted() returns a new list and
   accepts any iterable.

Q58. What is a docstring? Where is it stored?

A: The first string literal in a def/class/module; stored in __doc__, shown by
   help() and IDEs. It documents the contract, not the implementation.

Q59. Are type hints enforced at runtime?

A: No. They are metadata (__annotations__) for editors, mypy/pyright, and
   frameworks. Runtime validation needs pydantic or explicit checks.

Q60. What is the mutable-default rule in one sentence?

A: Never use a mutable object as a default; use None (or a sentinel) and create
   a fresh object inside the function.

--- DESIGN / RECURSION ---

Q61. What makes a good function?

A: One responsibility, a verb name, explicit inputs/outputs, validation at the
   boundary, no hidden global state, documented side effects, and testability.

Q62. What is a side effect?

A: Any observable interaction beyond returning a value: printing, mutating
   arguments/globals, file/network I/O, randomness, time. Necessary at the edges;
   dangerous when hidden in core logic.

Q63. What two parts must every recursive function have?

A: A base case that stops recursion and a recursive case that moves toward the
   base case. Otherwise: RecursionError.

Q64. Why is naive Fibonacci recursion slow?

A: It recomputes the same subproblems exponentially (O(2^n)). Memoise with
   functools.lru_cache (O(n)) or use the iterative O(n) time / O(1) space version.

Q65. Does Python optimise tail recursion?

A: No. Every call adds a frame, so deep recursion hits the limit (default 1000).
   Prefer iteration for deep/unbounded loops, or raise the limit deliberately.

Q66. When is recursion the right tool?

A: Tree/graph traversal, divide-and-conquer, backtracking, nested data
   (JSON/filesystem). It is a poor fit for simple linear repetition.

==============================================================================
PART 2 - PRACTICAL QUESTIONS (WITH RUNNABLE CODE)
==============================================================================
"""

# ------------------------------------------------------------------------------
# P1. Predict the output of basic string operations.
# ------------------------------------------------------------------------------
s = "Python"
print("P1:", s[0], s[-1], s[1:4], s[::-1])
# P1: P n yth nohtyP

print("P1:", s[10:20] == "", len(s[10:20]))
# P1: True 0

# ------------------------------------------------------------------------------
# P2. Explain concatenation vs repetition.
# ------------------------------------------------------------------------------
print("P2:", "5" + "3", "5" * 3, "ab" * 0 == "")
# P2: 53 555 True

# ------------------------------------------------------------------------------
# P3. Reverse the WORDS (not the characters) in a sentence.
# ------------------------------------------------------------------------------
sentence = "Python is fun to learn"
reversed_words = " ".join(sentence.split()[::-1])
print("P3:", reversed_words)
# P3: learn to fun is Python

# ------------------------------------------------------------------------------
# P4. Check whether a string is a palindrome (ignore case/punctuation).
# ------------------------------------------------------------------------------
def is_palindrome(text):
    """Return True if text reads the same forwards and backwards."""
    cleaned = [ch.casefold() for ch in text if ch.isalnum()]
    return cleaned == cleaned[::-1]

print("P4:", is_palindrome("A man, a plan, a canal: Panama"))
print("P4:", is_palindrome("Python"))
# P4: True
# P4: False

# ------------------------------------------------------------------------------
# P5. Count vowels and consonants.
# ------------------------------------------------------------------------------
def count_vowels_consonants(text):
    """Return (vowels, consonants), counting letters only."""
    vowels = consonants = 0
    for ch in text.casefold():
        if ch in "aeiou":
            vowels += 1
        elif ch.isalpha():
            consonants += 1
    return vowels, consonants

print("P5:", count_vowels_consonants("Hello World"))
# P5: (3, 7)

# ------------------------------------------------------------------------------
# P6. Check whether two strings are anagrams.
# ------------------------------------------------------------------------------
def are_anagrams(a, b):
    """Return True if a and b use the same letters with the same counts."""
    def clean(text):
        return sorted(ch for ch in text.casefold() if ch.isalnum())
    return clean(a) == clean(b)

print("P6:", are_anagrams("Listen", "Silent"))
print("P6:", are_anagrams("abc", "abd"))
# P6: True
# P6: False

# ------------------------------------------------------------------------------
# P7. Remove duplicate characters while preserving order.
# ------------------------------------------------------------------------------
def unique_chars(text):
    """Return text with duplicates removed, keeping first occurrences."""
    seen = set()
    result = []
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)
    return "".join(result)

print("P7:", unique_chars("banana"))
# P7: ban

# ------------------------------------------------------------------------------
# P8. Find the most frequent character (deterministic tie-break).
# ------------------------------------------------------------------------------
from collections import Counter

def most_frequent_char(text):
    """Return the most common character, ties broken alphabetically."""
    counts = Counter(ch for ch in text.casefold() if not ch.isspace())
    if not counts:
        return None
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]

print("P8:", most_frequent_char("banana"))
# P8: ('a', 3)

# ------------------------------------------------------------------------------
# P9. Run-length encoding.
# ------------------------------------------------------------------------------
def run_length_encode(text):
    """Encode runs: 'aaabbc' -> 'a3b2c1'."""
    if not text:
        return ""
    parts = []
    previous = text[0]
    count = 1
    for ch in text[1:]:
        if ch == previous:
            count += 1
        else:
            parts.append(f"{previous}{count}")
            previous = ch
            count = 1
    parts.append(f"{previous}{count}")
    return "".join(parts)

print("P9:", run_length_encode("aaabbc"))
# P9: a3b2c1

# ------------------------------------------------------------------------------
# P10. Use all three formatting styles for one record.
# ------------------------------------------------------------------------------
name, score = "Rohit", 91.5678
print("P10:", f"{name}: {score:.1f}")
print("P10:", "{}: {:.1f}".format(name, score))
print("P10:", "%s: %.1f" % (name, score))
# P10: Rohit: 91.6
# P10: Rohit: 91.6
# P10: Rohit: 91.6

# ------------------------------------------------------------------------------
# P11. Predict the string-method outputs.
# ------------------------------------------------------------------------------
print("P11:", " a  b ".split())
print("P11:", " a  b ".split(" "))
print("P11:", "a-b-c".split("-", 1))
print("P11:", "-".join(["a", "b", "c"]))
print("P11:", "banana".replace("a", "o", 2))
print("P11:", "xxhixx".strip("x"))
print("P11:", "abc".find("z"), "abc".count(""))
# P11: ['a', 'b']
# P11: ['', 'a', '', 'b', '']
# P11: ['a', 'b-c']
# P11: a-b-c
# P11: bonona
# P11: hi
# P11: -1 4

# ------------------------------------------------------------------------------
# P12. Demonstrate *args and **kwargs.
# ------------------------------------------------------------------------------
def show_args(*args, **kwargs):
    """Return the collected argument containers."""
    return args, kwargs

args, kwargs = show_args(1, 2, mode="fast")
print("P12:", args, type(args).__name__)
print("P12:", kwargs, type(kwargs).__name__)
# P12: (1, 2) tuple
# P12: {'mode': 'fast'} dict

# ------------------------------------------------------------------------------
# P13. Demonstrate the mutable default bug and the fix.
# ------------------------------------------------------------------------------
def buggy(value, bucket=[]):
    bucket.append(value)
    return bucket

print("P13 buggy:", buggy(1))
print("P13 buggy:", buggy(2))
# P13 buggy: [1]
# P13 buggy: [1, 2]   <- leaked state

def fixed(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket

print("P13 fixed:", fixed(1))
print("P13 fixed:", fixed(2))
# P13 fixed: [1]
# P13 fixed: [2]

# ------------------------------------------------------------------------------
# P14. Explain the output of a scope puzzle.
# ------------------------------------------------------------------------------
x = 10

def shadow():
    x = 20
    return x

print("P14:", shadow(), x)
# P14: 20 10

def read_global():
    return x

print("P14:", read_global())
# P14: 10

# UnboundLocalError: an assignment marks x local for the whole function.
# See 06_scope_legb.py for the full failing example.

# ------------------------------------------------------------------------------
# P15. Build a closure-based counter.
# ------------------------------------------------------------------------------
def make_counter():
    """Return a function that increments and returns a private count."""
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c1 = make_counter()
c2 = make_counter()
print("P15:", c1(), c1(), c1(), c2())
# P15: 1 2 3 1

# ------------------------------------------------------------------------------
# P16. lambda + map + filter + sorted.
# ------------------------------------------------------------------------------
numbers = [1, 2, 3, 4, 5, 6]
doubled_evens = list(map(lambda n: n * 2, filter(lambda n: n % 2 == 0, numbers)))
print("P16:", doubled_evens)
# P16: [4, 8, 12]

words = ["banana", "Apple", "cherry"]
print("P16:", sorted(words, key=str.casefold))
# P16: ['Apple', 'banana', 'cherry']

students = [("Rohit", 85), ("Amit", 92), ("Sara", 78)]
print("P16:", sorted(students, key=lambda s: -s[1]))
# P16: [('Amit', 92), ('Rohit', 85), ('Sara', 78)]

# ------------------------------------------------------------------------------
# P17. Late binding in a loop.
# ------------------------------------------------------------------------------
funcs = [lambda: i for i in range(3)]
print("P17:", [f() for f in funcs])
# P17: [2, 2, 2]

fixed_funcs = [lambda i=i: i for i in range(3)]
print("P17:", [f() for f in fixed_funcs])
# P17: [0, 1, 2]

# ------------------------------------------------------------------------------
# P18. Recursion: factorial, Fibonacci, flatten.
# ------------------------------------------------------------------------------
def factorial(n):
    """Return n! recursively."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return 1 if n < 2 else n * factorial(n - 1)

print("P18:", factorial(5))
# P18: 120

def flatten(items):
    """Flatten arbitrarily nested lists into one list."""
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print("P18:", flatten([1, [2, [3, 4]], 5]))
# P18: [1, 2, 3, 4, 5]

# ------------------------------------------------------------------------------
# P19. Docstring + type hints in one function.
# ------------------------------------------------------------------------------
def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its character length.

    Args:
        words: Words to measure.

    Returns:
        A dict from word to length.
    """
    return {word: len(word) for word in words}

print("P19:", word_lengths(["a", "bb", "ccc"]))
# P19: {'a': 1, 'bb': 2, 'ccc': 3}
print("P19:", word_lengths.__annotations__)
# P19: {'words': list[str], 'return': dict[str, int]}
# (Exact repr can vary slightly by Python version; the keys are the important part.)

# ------------------------------------------------------------------------------
# P20. Code review: spot three problems.
# ------------------------------------------------------------------------------
# def process(items, results=[]):
#     for i in items:
#         if i > 0:
#             results.append(i * 2)
#             print(results)
#     tax_rate = 0.18
#     return results
#
# Problems:
#   1) Mutable default 'results=[]' leaks state between calls.
#   2) Printing inside a calculation function is a hidden side effect;
#      return the value and let the caller display it.
#   3) 'tax_rate' is unused (and if it were used, a hidden global would be a
#      better discussion point than a magic number).
#   4) Name 'process' is vague; 'double_positive' states the behaviour.
# A better shape:
def double_positive(items, results=None):
    """Return positive items doubled, without mutating shared state."""
    output = [] if results is None else list(results)
    output.extend(i * 2 for i in items if i > 0)
    return output

print("P20:", double_positive([-1, 2, 3]))
# P20: [4, 6]


if __name__ == "__main__":
    print("\nAll Day 3 interview snippets ran successfully.")
