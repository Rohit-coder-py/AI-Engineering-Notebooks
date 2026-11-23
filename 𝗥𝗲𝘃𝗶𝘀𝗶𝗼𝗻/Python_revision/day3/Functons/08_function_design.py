"""
================================================================================
DAY 3 - C. FUNCTION DESIGN + RECURSION
================================================================================

INTERVIEW MINDSET
-----------------
Interviewers judge design through small choices:
  * Does the function do ONE thing?
  * Does it RETURN a result instead of printing and mutating globals?
  * Are inputs validated at the boundary?
  * Are side effects explicit?
  * Is the mutable-default trap avoided?
  * Can it be tested without a database, network, or stdin?

Say: "I keep functions small and pure where possible, pass dependencies as
      arguments, return values instead of mutating shared state, and push I/O
      to the edges of the program."
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. ONE RESPONSIBILITY PER FUNCTION
# ------------------------------------------------------------------------------
# A function should have one reason to change. If describing it needs "and",
# split it.
#
# BAD: process_order() validates, computes tax, writes to a database, and prints
# GOOD: validate_order(), calculate_total(), save_order(), format_receipt()

def validate_order(order):
    """Return a list of validation errors (empty means valid).

    Args:
        order: Dict with 'items' (list of dicts) and optional 'discount'.

    Returns:
        A list of human-readable error strings.
    """
    errors = []
    if not order.get("items"):
        errors.append("order must contain at least one item")
    for item in order.get("items", []):
        if item.get("price", 0) < 0:
            errors.append(f"negative price for {item.get('name', '?')}")
        if item.get("quantity", 0) <= 0:
            errors.append(f"invalid quantity for {item.get('name', '?')}")
    if not 0 <= order.get("discount", 0) <= 100:
        errors.append("discount must be between 0 and 100")
    return errors

def calculate_subtotal(order):
    """Return the sum of price * quantity for all items."""
    return sum(i["price"] * i["quantity"] for i in order["items"])

def calculate_total(order):
    """Return subtotal after discount, with 18% tax applied."""
    subtotal = calculate_subtotal(order)
    discount = subtotal * order.get("discount", 0) / 100
    taxable = subtotal - discount
    return round(taxable * 1.18, 2)

def format_receipt(order, total):
    """Return a printable receipt string."""
    lines = [f"{i['name']} x{i['quantity']}: {i['price'] * i['quantity']:.2f}"
             for i in order["items"]]
    lines.append(f"TOTAL: {total:.2f}")
    return "\n".join(lines)

# Each function is independently testable.
demo_order = {
    "items": [
        {"name": "book", "price": 500, "quantity": 2},
        {"name": "pen", "price": 20, "quantity": 5},
    ],
    "discount": 10,
}
print(validate_order(demo_order))        # []
total = calculate_total(demo_order)
print(total)                             # 1168.2
print(format_receipt(demo_order, total))

# INTERVIEW NOTE:
#   This separation is also what makes unit testing easy: no I/O in the
#   calculation functions, so tests are fast and deterministic.


# ------------------------------------------------------------------------------
# 2. PURE FUNCTIONS vs SIDE EFFECTS
# ------------------------------------------------------------------------------
# PURE:
#   * same inputs -> same output
#   * no observable side effects (no printing, no file/network, no mutation
#     of external state)
#
# IMPURE:
#   * prints, writes files, updates a global, mutates an argument, uses random
#     or time, reads stdin, etc.

def add_tax_pure(amount, rate):
    """Return amount plus tax (pure)."""
    return amount * (1 + rate)

print(add_tax_pure(100, 0.18))   # 118.0

# Impure: mutates the caller's list.
def add_bad(item, bucket):
    bucket.append(item)           # side effect on the caller's object
    return bucket

my_list = []
add_bad("x", my_list)
print(my_list)                    # ['x']  <- caller surprised

# Pure alternative: return a NEW list.
def add_good(item, bucket):
    """Return a new list with item appended (pure)."""
    return [*bucket, item]

my_list = []
new_list = add_good("x", my_list)
print(my_list, new_list)          # [] ['x']

# Impure is not "bad" - it is necessary at the edges (I/O, UI, database).
# The design rule is: keep the CORE logic pure; push side effects to the edges.

# INTERVIEW NOTE:
#   "Side effect" does not mean "bug". It means an observable interaction with
#   the outside world. The problem is HIDDEN side effects.

# Mutable arguments: document whether you mutate or copy.
def append_in_place(items, value):
    """Append value to items IN PLACE and return None (like list.append)."""
    items.append(value)

def appended_copy(items, value):
    """Return a NEW list with value appended (input unchanged)."""
    return items + [value]


# ------------------------------------------------------------------------------
# 3. AVOID UNNECESSARY GLOBALS
# ------------------------------------------------------------------------------
# Global mutable state makes functions depend on history, breaks tests, and
# creates hidden coupling. Pass what you need; return what changed.

# BAD: hidden dependency on a global.
tax_rate = 0.18

def total_with_global(amount):
    return amount * (1 + tax_rate)

print(total_with_global(100))    # 118.0

# GOOD: explicit dependency.
def total_with_rate(amount, rate):
    """Return amount including tax at the given rate."""
    return amount * (1 + rate)

print(total_with_rate(100, 0.18))

# For configuration that truly is app-wide, a module-level constant is fine
# (read-only). The problem is MUTABLE global state, not constants.

# INTERVIEW NOTE:
#   "Why avoid globals?" -> harder to test, hidden coupling, race conditions,
#   and action-at-a-distance. Pass state explicitly or use a small class.


# ------------------------------------------------------------------------------
# 4. THE MUTABLE DEFAULT TRAP (DESIGN VIEW)
# ------------------------------------------------------------------------------
# Defaults are evaluated once at definition time. With a mutable default, all
# calls share the same object.

def collect_bad(value, results=[]):
    results.append(value)
    return results

print(collect_bad(1))            # [1]
print(collect_bad(2))            # [1, 2]  <- state leak

# Fix with None sentinel:
def collect_good(value, results=None):
    """Return a list with value appended, creating a new list by default."""
    if results is None:
        results = []
    results.append(value)
    return results

print(collect_good(1))           # [1]
print(collect_good(2))           # [2]

# Rule: use only IMMUTABLE defaults (None, numbers, strings, tuples, frozenset).
# In dataclasses, use field(default_factory=list) for the same reason.

# INTERVIEW FOLLOW-UP:
#   "Why does Python evaluate defaults once?" -> It is part of the function
#   object, stored in __defaults__. Re-evaluating on every call would cost
#   performance and break intentional "shared default" use cases.

# INTERVIEW FOLLOW-UP:
#   "Is using None as a sentinel always safe?" -> Only if None is not a valid
#   input. If None is meaningful, use a unique sentinel object:
SENTINEL = object()

def collect_safe(value, results=SENTINEL):
    """Append to results, treating SENTINEL as 'no list supplied'."""
    if results is SENTINEL:
        results = []
    results.append(value)
    return results


# ------------------------------------------------------------------------------
# 5. COMPOSITION: SMALL FUNCTIONS, BIG BEHAVIOUR
# ------------------------------------------------------------------------------
# Build complex behaviour by composing small, named steps. This is easier to
# read, test, and change than one large function.

def clean_text(text):
    """Lowercase and collapse whitespace."""
    return " ".join(text.lower().split())

def tokenize(text):
    """Split cleaned text into words."""
    return clean_text(text).split()

def word_frequencies(text):
    """Return a dict mapping word -> count."""
    freq = {}
    for word in tokenize(text):
        freq[word] = freq.get(word, 0) + 1
    return freq

def top_words(text, n=3):
    """Return the n most frequent words as (word, count) tuples."""
    freq = word_frequencies(text)
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]

sample = "The quick brown fox. The lazy dog. The fox runs!"
print(top_words(sample, 2))      # [('the', 3), ('fox', 2)]

# INTERVIEW NOTE:
#   This is the same decomposition used in the Day 3 Text Analyser project
#   (file 10). Mention it when asked "how would you structure this program?"


# --------------------------------------------------------------------------
# 6. RECURSION (FUNDAMENTALS)
# --------------------------------------------------------------------------
# A recursive function calls itself on a SMALLER input.
# Every recursion needs:
#   1) a BASE CASE that stops the recursion, and
#   2) a RECURSIVE CASE that moves toward the base case.
# Without a base case (or with a wrong step) you get RecursionError.

def factorial(n):
    """Return n! for a non-negative integer n."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n in (0, 1):              # base case
        return 1
    return n * factorial(n - 1)  # recursive case

print(factorial(0))              # 1
print(factorial(5))              # 120
print(factorial(10))             # 3628800

# How factorial(4) unfolds:
#   factorial(4) = 4 * factorial(3)
#                = 4 * 3 * factorial(2)
#                = 4 * 3 * 2 * factorial(1)
#                = 4 * 3 * 2 * 1
#                = 24

# Each pending call waits on the stack. Deep recursion can overflow it.
import sys
print(sys.getrecursionlimit())   # typically 1000

def infinite(n):
    return infinite(n + 1)

try:
    infinite(0)
except RecursionError as exc:
    print("RecursionError:", exc)   # maximum recursion depth exceeded

# INTERVIEW NOTE:
#   Python does NOT optimise tail calls. A "tail-recursive" function still
#   grows the stack. Use iteration for deep or unbounded loops.

# Recursion on a sequence: sum a list.
def recursive_sum(numbers):
    """Return the sum of a list using recursion."""
    if not numbers:              # base case: empty list
        return 0
    return numbers[0] + recursive_sum(numbers[1:])   # O(n^2) due to slicing

print(recursive_sum([1, 2, 3, 4]))   # 10

# Better version uses an index (avoids copying slices):
def recursive_sum_fast(numbers, index=0):
    """Return the sum starting at index (no slicing)."""
    if index == len(numbers):
        return 0
    return numbers[index] + recursive_sum_fast(numbers, index + 1)

print(recursive_sum_fast([1, 2, 3, 4]))   # 10

# Naive Fibonacci: elegant but EXPONENTIAL - a classic interview discussion.
def fib_naive(n):
    """Return the n-th Fibonacci number (exponential time)."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

print(fib_naive(10))             # 55

# Memoisation turns it into O(n) by caching results.
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    """Return the n-th Fibonacci number (memoised)."""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))                   # 12586269025 (fast)
print(fib.cache_info())          # hits, misses, maxsize, currsize

# Iterative version: O(n) time, O(1) space - usually the best answer.
def fib_iterative(n):
    """Return the n-th Fibonacci number iteratively."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib_iterative(50))         # 12586269025

# Recursion is a good fit for:
#   * tree/graph traversal (filesystem, JSON, DOM)
#   * divide-and-conquer (merge sort, binary search)
#   * backtracking (permutations, sudoku)
# Iteration is a better fit for simple linear repetition and deep loops.

# Palindrome check with recursion (interview exercise):
def is_palindrome(text):
    """Return True if text reads the same forwards and backwards.

    Ignores case, spaces, and punctuation.
    """
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    def check(lo, hi):
        if lo >= hi:
            return True
        if cleaned[lo] != cleaned[hi]:
            return False
        return check(lo + 1, hi - 1)
    return check(0, len(cleaned) - 1)

print(is_palindrome("A man, a plan, a canal: Panama"))   # True
print(is_palindrome("Python"))                            # False


# ------------------------------------------------------------------------------
# 7. THE __main__ GUARD
# ------------------------------------------------------------------------------
# When a module is imported, its top-level code runs - unless guarded.
# The guard makes a file both importable and runnable.

def main():
    """Run a small demonstration."""
    print("demo total:", total_with_rate(200, 0.18))

if __name__ == "__main__":
    main()

# INTERVIEW NOTE:
#   __name__ is "__main__" only when the file is executed directly. When
#   imported, __name__ is the module name. This prevents import side effects
#   and is standard for scripts and tests.


# ------------------------------------------------------------------------------
# 8. FUNCTION DESIGN CHECKLIST
# ------------------------------------------------------------------------------
# [ ] Does one thing; the name is a verb phrase.
# [ ] Returns a value; printing is left to the caller/UI layer.
# [ ] Inputs are parameters, not hidden globals.
# [ ] Validates inputs at the boundary and fails fast with clear errors.
# [ ] No mutable default arguments.
# [ ] Side effects are explicit and documented.
# [ ] Small enough to read on one screen.
# [ ] Has a docstring and (ideally) type hints.
# [ ] Handles edge cases: empty input, zero, None, invalid types.
# [ ] Is testable without I/O.
# [ ] Recursion has a base case and moves toward it.
#
# INTERVIEW ONE-LINER:
#   "I optimise for the next reader: a clear name, a single responsibility,
#    explicit inputs/outputs, and no hidden state."
# ================================================================================
