"""
================================================================================
DAY 3 - B1. FUNCTION FUNDAMENTALS
================================================================================

INTERVIEW MINDSET
-----------------
Do NOT say: "A function is a block of code you can reuse."

DO say:     "A function is a NAMED, CALLABLE OBJECT that encapsulates a
             behaviour. It has a parameter list, a body, an optional
             docstring, and it RETURNS a value (None if no return is given).
             Functions are first-class objects: they can be assigned, passed,
             returned, and stored in data structures."

Why functions exist (the four real reasons):
  1) Abstraction   - name an idea; hide the details.
  2) Reuse         - write once, call many times.
  3) Testability   - a small unit with clear inputs/outputs is easy to test.
  4) Manageability - local names, smaller surface area, easier debugging.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. DEFINING AND CALLING A FUNCTION
# ------------------------------------------------------------------------------
# def name(parameters):
#     """docstring"""
#     body
#     return value
#
# Defining a function does NOT run the body. It creates a function object and
# binds the name to it. The body runs only when the function is CALLED.

def greet():
    """Print a fixed greeting."""
    print("Hello, world!")

# The def statement has already executed; greet is now a function object.
print(type(greet))               # <class 'function'>
print(greet.__name__)            # greet

greet()                          # Hello, world!  <- body runs now
greet()                          # callable any number of times


# ------------------------------------------------------------------------------
# 2. PARAMETERS vs ARGUMENTS
# ------------------------------------------------------------------------------
# PARAMETERS are the names in the function DEFINITION (formal parameters).
# ARGUMENTS are the actual values supplied at the CALL SITE.
# People use the words loosely; interviewers like the precise distinction.

def introduce(name, city):
    """Return a sentence introducing a person."""
    return f"{name} lives in {city}."

# 'name' and 'city' are parameters.
# '"Rohit"' and '"Pune"' are arguments.
print(introduce("Rohit", "Pune"))    # Rohit lives in Pune.

# A function can have zero or many parameters.
def no_params():
    return 42

print(no_params())               # 42


# ------------------------------------------------------------------------------
# 3. RETURN VALUES vs print()
# ------------------------------------------------------------------------------
# print()  -> sends text to stdout; its OWN return value is None.
# return   -> hands a value back to the caller; ENDS the function immediately.
#
# This distinction is one of the most common junior-interview filters.

def add_and_print(a, b):
    print(a + b)                 # displays 5, but returns None

def add_and_return(a, b):
    return a + b                 # returns 5 to the caller

result_printed = add_and_print(2, 3)   # prints 5
result_returned = add_and_return(2, 3)

print(result_printed)            # None
print(result_returned)           # 5

# A function with no return statement returns None implicitly.
def do_nothing():
    pass

print(do_nothing())              # None

# 'return' with no value also returns None.
def early_exit():
    return

print(early_exit())              # None

# Because the returned value can be used, return-based functions COMPOSE.
total = add_and_return(2, 3) * 10
print(total)                     # 50

# print-based functions cannot be composed like that:
# add_and_print(2, 3) * 10       # TypeError: NoneType * int

# INTERVIEW ONE-LINER:
#   "print() is for humans; return is for the program. A function that only
#    prints is hard to test and impossible to reuse in a calculation."


# ------------------------------------------------------------------------------
# 4. RETURNING MULTIPLE VALUES (REALLY A TUPLE)
# ------------------------------------------------------------------------------
# Python returns a single object. With commas, that object is a TUPLE,
# which the caller can unpack.

def min_max(numbers):
    """Return the smallest and largest values as a tuple."""
    return min(numbers), max(numbers)

result = min_max([4, 1, 9, 2])
print(result)                    # (1, 9)
print(type(result))              # <class 'tuple'>

low, high = min_max([4, 1, 9, 2])   # tuple unpacking
print(low, high)                 # 1 9

# Returning a tuple is fine; returning a dict or a dataclass is better when
# the meaning of each field is not obvious at the call site.
def stats(numbers):
    """Return descriptive stats as a dict for readability."""
    return {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "total": sum(numbers),
    }

s = stats([4, 1, 9, 2])
print(s["total"])                # 16


# ------------------------------------------------------------------------------
# 5. EARLY RETURN (GUARD CLAUSES)
# ------------------------------------------------------------------------------
# Prefer early returns over deeply nested if/else. It flattens the code and
# makes the "happy path" obvious.

def classify_score(score):
    """Return a grade for a numeric score."""
    if not isinstance(score, (int, float)):
        return "invalid: not a number"
    if score < 0 or score > 100:
        return "invalid: out of range"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"

print(classify_score(95))        # A
print(classify_score(72))        # C
print(classify_score(-1))        # invalid: out of range
print(classify_score("95"))      # invalid: not a number

# INTERVIEW NOTE:
#   Guard clauses + a single final return is a readability pattern interviewers
#   notice. It also avoids the "arrow anti-pattern" of nested ifs.


# ------------------------------------------------------------------------------
# 6. FUNCTIONS ARE OBJECTS (FIRST-CLASS)
# ------------------------------------------------------------------------------
# A function is a value like any other. This is the foundation of callbacks,
# decorators, map/filter, and dependency injection.

def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

# Assign to another name:
louder = shout
print(louder("hello"))           # HELLO!

# Store in a data structure:
formatters = {"loud": shout, "soft": whisper}
print(formatters["soft"]("HELLO"))   # hello...

# Pass as an argument (higher-order function):
def apply_twice(func, value):
    """Apply func to value two times."""
    return func(func(value))

print(apply_twice(shout, "hi"))  # HI!!

# Return a function (closure / factory):
def make_multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10), triple(10))    # 20 30

# INTERVIEW NOTE:
#   Functions being first-class is why decorators work: a decorator takes a
#   function, wraps it, and returns a new function object.


# ------------------------------------------------------------------------------
# 7. WHEN DOES THE CODE RUN?
# ------------------------------------------------------------------------------
# At DEFINITION time Python:
#   * compiles the body,
#   * evaluates default argument values,
#   * creates the function object,
#   * binds the name.
# It does NOT execute the body.
#
# At CALL time Python:
#   * binds arguments to parameters in a new LOCAL scope,
#   * executes the body,
#   * returns the result,
#   * destroys the local scope (unless a closure keeps it alive).

print("before def")

def demo_order():
    print("inside body")

print("after def, before call")   # body has NOT run yet
demo_order()                      # now the body runs
print("after call")

# Output order:
#   before def
#   after def, before call
#   inside body
#   after call


# ------------------------------------------------------------------------------
# 8. DOCSTRINGS AND help()
# ------------------------------------------------------------------------------
# A docstring is the first statement in a function/class/module, written with
# triple quotes. Python stores it on __doc__; help() and IDEs read it.

def area_of_rectangle(length, width):
    """Return the area of a rectangle.

    Args:
        length: Positive length in metres.
        width: Positive width in metres.

    Returns:
        The area in square metres.

    Raises:
        ValueError: If either dimension is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("dimensions must be non-negative")
    return length * width

print(area_of_rectangle.__doc__.splitlines()[0])   # Return the area of a rectangle.
print(area_of_rectangle(3, 4))                     # 12

# INTERVIEW NOTE:
#   Docstrings are for CONSUMERS of the function (what/why/contract).
#   Comments are for MAINTAINERS (why this implementation choice).
#   Do not narrate obvious code with comments; explain intent.


# ------------------------------------------------------------------------------
# 9. NAMING AND SIZE
# ------------------------------------------------------------------------------
# * Use verbs for functions: calculate_tax, load_config, is_valid.
# * Use snake_case (PEP 8).
# * A function should do ONE thing; if the name needs "and", split it.
# * Aim for a small number of parameters (<= 3-4). Beyond that, pass an object.
# * Return values; avoid printing inside business logic.
#
# BAD:  def process(data): ... does validation + parsing + saving + printing
# GOOD: validate(data), parse(data), save(record), render(report)


# ------------------------------------------------------------------------------
# 10. INTERVIEW GOTCHAS - QUICK REFERENCE
# ------------------------------------------------------------------------------
# Q: What does a function return if there is no return statement?
# A: None.
#
# Q: Can a function return multiple values?
# A: It returns one tuple; the caller can unpack it.
#
# Q: Difference between print() and return?
# A: print displays; return hands a value back and exits the function.
#
# Q: Are functions objects?
# A: Yes - first-class: assignable, passable, returnable, storable.
#
# Q: When are default arguments evaluated?
# A: Once, at definition time (important for mutable defaults - see file 05).
#
# Q: Can you define a function inside a function?
# A: Yes. The inner function is local; it can close over outer variables.
#
# Q: Does defining a function execute its body?
# A: No. Only the def statement runs; the body runs on each call.
#
# Q: What is a pure function?
# A: Same inputs -> same output, no side effects. Easy to test and reason about.
#    (Covered in depth in file 08.)
# ================================================================================
