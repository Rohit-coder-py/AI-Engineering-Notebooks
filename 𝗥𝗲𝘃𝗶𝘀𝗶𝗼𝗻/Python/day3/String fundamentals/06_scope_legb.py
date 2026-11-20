"""
================================================================================
DAY 3 - B3. SCOPE AND THE LEGB RULE
================================================================================

INTERVIEW MINDSET
-----------------
Say: "Python resolves names with the LEGB rule - Local, Enclosing, Global,
      Built-in - determined at COMPILE time (lexical scope), not at call time.
      Assignment inside a function makes a name local unless it is declared
      global or nonlocal. Reading an outer name is fine; rebinding it requires
      a declaration."

Why interviewers ask:
  * UnboundLocalError is a classic debugging question.
  * Closures and decorators depend on nonlocal/global knowledge.
  * "Avoid globals" is a design discussion, not just syntax.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. THE FOUR SCOPES
# ------------------------------------------------------------------------------
# L - Local      : names assigned inside the current function
# E - Enclosing  : names in an outer function (for nested functions)
# G - Global     : names at module level (the .py file)
# B - Built-in   : names Python provides (len, print, sum, ...)
#
# Python looks L -> E -> G -> B and uses the FIRST match.
# If none is found: NameError.

module_level = "global"

def outer():
    enclosing_level = "enclosing"

    def inner():
        local_level = "local"
        # Lookup order for these names:
        print(local_level)        # L
        print(enclosing_level)    # E
        print(module_level)       # G
        print(len("abc"))         # B

    inner()

outer()
# local
# enclosing
# global
# 3


# ------------------------------------------------------------------------------
# 2. LOCAL SCOPE
# ------------------------------------------------------------------------------
# Every function call creates a NEW local namespace. Names assigned in the
# body are local by default. They disappear when the function returns.

def make_greeting():
    message = "hello"            # local to make_greeting
    return message

print(make_greeting())           # hello

try:
    print(message)
except NameError as exc:
    print("NameError:", exc)     # name 'message' is not defined

# IMPORTANT: scope is decided by the COMPILER, not by execution order.
# If a name is assigned ANYWHERE in a function, it is local for the WHOLE
# function. Reading it before the assignment raises UnboundLocalError.

counter = 10

def broken():
    print(counter)               # Python already marked 'counter' as local
    counter = 20                 # because of this assignment

try:
    broken()
except UnboundLocalError as exc:
    print("UnboundLocalError:", exc)
    # cannot access local variable 'counter' where it is not associated with a value

# The fix depends on intent:
#   * want to use the global? remove the assignment, or declare 'global'.
#   * want a local? assign before reading.

def fixed_read():
    print(counter)               # reads the global (no assignment -> not local)

fixed_read()                     # 10

def fixed_local():
    counter = 20                 # brand-new local name
    print(counter)

fixed_local()                    # 20
print(counter)                   # 10  (global unchanged)


# ------------------------------------------------------------------------------
# 3. GLOBAL SCOPE AND THE global KEYWORD
# ------------------------------------------------------------------------------
# Reading a global inside a function needs NO declaration.
# REBINDING a global (including +=, which is read + assign) REQUIRES 'global'.

total = 0

def add_to_total_bad(amount):
    total += amount              # UnboundLocalError: total is local here

try:
    add_to_total_bad(5)
except UnboundLocalError as exc:
    print("UnboundLocalError:", exc)

def add_to_total(amount):
    global total                 # declare intent: use the module-level name
    total += amount

add_to_total(5)
add_to_total(7)
print(total)                     # 12

# 'global' must appear before any use of the name in that function.
# A function can declare several: global a, b

# WARNING: 'global' is often a code smell. Prefer passing values in and
# returning results out. Global state makes testing and reasoning harder.

# INTERVIEW NOTE:
#   MUTATING a global container does NOT require 'global':
items = []

def append_item(x):
    items.append(x)              # mutation, not rebinding -> allowed

append_item(1)
print(items)                     # [1]

def rebind_items():
    global items
    items = [99]                 # rebinding -> requires global

rebind_items()
print(items)                     # [99]

# This mutation-vs-rebinding distinction is a frequent follow-up question.


# ------------------------------------------------------------------------------
# 4. ENCLOSING SCOPE AND nonlocal
# ------------------------------------------------------------------------------
# A nested function can READ names from the enclosing function.
# To REBIND an enclosing name, declare it 'nonlocal'.
# nonlocal searches enclosing function scopes only - never the global scope.

def make_counter():
    count = 0

    def increment():
        nonlocal count           # bind to make_counter's 'count'
        count += 1
        return count

    return increment

counter_a = make_counter()
counter_b = make_counter()       # a separate closure with its own count

print(counter_a())               # 1
print(counter_a())               # 2
print(counter_b())               # 1  (independent state)

# Without nonlocal, the inner assignment creates a local and the outer
# variable is never updated:
def make_counter_broken():
    count = 0

    def increment():
        count = 0                # local, shadows the outer name
        count += 1
        return count

    return increment

broken_counter = make_counter_broken()
print(broken_counter())          # 1
print(broken_counter())          # 1  (resets every call)

# nonlocal requires an existing binding in an enclosing function.
# At module level there is no enclosing function -> SyntaxError.
# def bad():
#     nonlocal x                   # SyntaxError: no binding for nonlocal 'x' found
#     x = 1

# INTERVIEW NOTE:
#   'global' -> module scope.  'nonlocal' -> nearest enclosing function scope.
#   'nonlocal' is what makes closure-based state (counters, accumulators) work.


# ------------------------------------------------------------------------------
# 5. CLOSURES (THE PRACTICAL USE OF ENCLOSING SCOPE)
# ------------------------------------------------------------------------------
# A closure is a function that remembers names from the scope where it was
# created, even after that scope has returned.

def make_multiplier(factor):
    """Return a function that multiplies its argument by factor."""
    def multiply(x):
        return x * factor        # 'factor' is captured from the enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(21))                # 42
print(triple(7))                 # 21

# Inspect the captured cells:
print(double.__closure__)              # (<cell at ...>,)
print(double.__closure__[0].cell_contents)   # 2

# Each call to make_multiplier creates a NEW scope, so each returned function
# has its own captured value.

# Classic closure gotcha: late binding in loops.
funcs = []
for i in range(3):
    funcs.append(lambda: i)      # captures the VARIABLE, not its current value

print([f() for f in funcs])      # [2, 2, 2]  (all see the final i)

# Fix 1: capture the value with a default argument.
funcs_ok = []
for i in range(3):
    funcs_ok.append(lambda i=i: i)
print([f() for f in funcs_ok])   # [0, 1, 2]

# Fix 2: use a factory function (a new scope per iteration).
def make_constant(value):
    return lambda: value

funcs_factory = [make_constant(i) for i in range(3)]
print([f() for f in funcs_factory])   # [0, 1, 2]

# INTERVIEW NOTE:
#   The lambda body is executed LATER; by then the loop has finished and 'i'
#   holds its final value. Default arguments are evaluated at definition time,
#   which is why fix 1 works.


# ------------------------------------------------------------------------------
# 6. COMPREHENSION SCOPE (PYTHON 3)
# ------------------------------------------------------------------------------
# Comprehensions have their own scope. Their loop variable does NOT leak into
# the surrounding scope (unlike Python 2).

x = 100
squares = [x * x for x in range(4)]
print(squares)                   # [0, 1, 4, 9]
print(x)                         # 100  (unchanged)

# But a comprehension CAN read names from the enclosing scope:
factor = 10
scaled = [n * factor for n in range(3)]
print(scaled)                    # [0, 10, 20]

# Class-body quirk: a comprehension inside a class body cannot see class
# attributes directly, because the class scope is not an enclosing FUNCTION
# scope. Use a method, or iterate over a module/global name.
try:
    class Example:
        values = [1, 2, 3]
        doubled = [v * 2 for v in values]   # NameError at class creation
except NameError as exc:
    print("NameError:", exc)     # name 'values' is not defined

# Correct approach: compute inside a method (or in __init__), where 'self'
# gives access to the attribute.
class ExampleFixed:
    values = [1, 2, 3]

    def doubled_values(self):
        """Return each class-level value doubled."""
        return [v * 2 for v in self.values]

print(ExampleFixed().doubled_values())   # [2, 4, 6]


# ------------------------------------------------------------------------------
# 7. BUILT-IN SCOPE AND SHADOWING
# ------------------------------------------------------------------------------
# Built-in names can be shadowed. This is legal but usually a bug.

print(len("abc"))                # 3

len = 5                          # shadows the built-in in this module
try:
    len("abc")
except TypeError as exc:
    print("TypeError:", exc)     # 'int' object is not callable

del len                          # remove the module-level shadow
print(len("abc"))                # 3  (built-in visible again)

# Never name variables list, dict, str, sum, min, max, id, type, input, etc.
# Use names like items, mapping, text, total, smallest, largest, identifier.

# builtins can also be inspected:
import builtins
print(builtins.abs(-3))          # 3


# ------------------------------------------------------------------------------
# 8. globals() AND locals() (AWARENESS)
# ------------------------------------------------------------------------------
# globals() returns the module namespace dict (live, not a copy).
# locals() returns a snapshot-like dict of the current local namespace.
# Modifying locals() is not guaranteed to affect actual local variables.

def inspect_scopes():
    local_var = 1
    print("local_var" in locals())        # True
    print("inspect_scopes" in globals())  # True

inspect_scopes()

# INTERVIEW NOTE:
#   Do not build programs around globals()/locals(). They are diagnostic tools.
#   Reaching for them usually signals a design problem.


# ------------------------------------------------------------------------------
# 9. WHY SCOPE IS LEXICAL (STATIC)
# ------------------------------------------------------------------------------
# A function uses the scope where it was DEFINED, not where it is CALLED.
# This is why closures work and why moving a function to another module can
# change which globals it sees.

def show_origin():
    return module_level

def call_it(func):
    module_level = "local to call_it"   # does NOT affect show_origin
    return func()

print(call_it(show_origin))      # global

# INTERVIEW ONE-LINER:
#   "Python scope is lexical (static), not dynamic."


# ------------------------------------------------------------------------------
# 10. INTERVIEW GOTCHAS - QUICK REFERENCE
# ------------------------------------------------------------------------------
# Q: What is the LEGB rule?
# A: Local -> Enclosing -> Global -> Built-in name resolution order.
#
# Q: Difference between global and nonlocal?
# A: global targets the module scope; nonlocal targets the nearest enclosing
#    function scope. Both are needed only for REBINDING.
#
# Q: Why does this raise UnboundLocalError?
#       x = 1
#       def f():
#           print(x)
#           x = 2
# A: The assignment makes x local for the whole function; it is read before
#    being bound. Fix: declare global x, or remove the assignment.
#
# Q: Do you need global to read a global?
# A: No. Only to rebind it.
#
# Q: Do you need global to mutate a global list?
# A: No. append() mutates the object; it does not rebind the name.
#
# Q: Does a comprehension leak its loop variable?
# A: No in Python 3; comprehensions have their own scope.
#
# Q: Why does a lambda in a loop capture the last value?
# A: Closures capture variables, not values. Bind the current value with a
#    default argument or a factory.
#
# Q: Can a nested function modify an enclosing variable without nonlocal?
# A: Only by mutating a mutable object. Rebinding requires nonlocal.
#
# Q: Are local variables created at call time or compile time?
# A: The compiler decides which names are local; the namespace is created per
#    call and values are bound as execution reaches the assignments.
# ================================================================================
