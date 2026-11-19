"""
================================================================================
DAY 1 — Dynamic Typing (and Static vs Dynamic vs Strong vs Weak)
================================================================================

INTERVIEW MINDSET: Be precise with terminology. Python is DYNAMICALLY typed
(type checked at runtime) AND STRONGLY typed (no silent implicit coercion).
Duck typing: "If it walks like a duck and quacks like a duck, it's a duck."
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. DYNAMIC TYPING IN ACTION
# ------------------------------------------------------------------------------
# A name has no fixed type — it simply refers to whatever object was last
# assigned to it. The type travels with the OBJECT, not the NAME.

value = 10
print(value, type(value))       # 10 <class 'int'>

value = 3.14
print(value, type(value))       # 3.14 <class 'float'>

value = "now I am a string"
print(value, type(value))       # now I am a string <class 'str'>

value = [1, 2, 3]
print(value, type(value))       # [1, 2, 3] <class 'list'>

# ------------------------------------------------------------------------------
# 2. type() vs isinstance()
# ------------------------------------------------------------------------------
x = 5
print(type(x) is int)           # True
print(isinstance(x, int))       # True

# bool is a subclass of int — interview trap!
print(isinstance(True, int))    # True
print(issubclass(bool, int))    # True
print(True + True)              # 2   (True==1, False==0)

# Prefer isinstance() over type() is ... because it honors inheritance.
class Animal: pass
class Dog(Animal): pass

d = Dog()
print(type(d) is Animal)        # False
print(isinstance(d, Animal))    # True   <- safer for polymorphic code

# ------------------------------------------------------------------------------
# 3. DUCK TYPING
# ------------------------------------------------------------------------------
# We don't check the TYPE; we check whether the object SUPPORTS the operation.

def quack(duck):
    duck.quack()

class RealDuck:
    def quack(self):
        print("Quack!")

class Person:
    def quack(self):
        print("I'm imitating a duck!")

quack(RealDuck())   # Quack!
quack(Person())     # I'm imitating a duck!   (no inheritance needed)

# Common interview example: anything with .read() works like a file.

# ------------------------------------------------------------------------------
# 4. STRONG TYPING (no silent coercion)
# ------------------------------------------------------------------------------
# Python will NOT implicitly convert between unrelated types.

print(5 + 3.2)        # 8.2   (numeric coercion is allowed — both are numbers)

try:
    print("5" + 2)     # TypeError: can only concatenate str (not "int") to str
except TypeError as e:
    print("Caught:", e)

# Explicit conversion is required:
print(int("5") + 2)   # 7

# ------------------------------------------------------------------------------
# 5. WHEN DYNAMIC TYPING BITES YOU (interview stories)
# ------------------------------------------------------------------------------
# A function documented to take an int may receive a string at runtime.
# Defensive checks / type hints help document intent (not enforce at runtime).

def process_count(n: int) -> int:          # : int and -> int are HINTS only
    return n * 2

print(process_count(5))        # 10
print(process_count("5"))      # "55"  — ran fine! Type hints are not enforced.

# Use isinstance() if you truly need runtime enforcement:
def process_count_strict(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be a non-bool int")
    return n * 2

# ------------------------------------------------------------------------------
# INTERVIEW NOTES
# ------------------------------------------------------------------------------
# Q: Static vs dynamic typing?
# A: Static = types checked at compile time (Java, C++). Dynamic = at runtime (Python).
#
# Q: Strong vs weak typing?
# A: Strong = no implicit type coercion (Python). Weak = implicit coercion (JS).
#    Python = dynamic + strong.
#
# Q: Are type hints enforced?
# A: No. They are metadata for tools (mypy, IDEs) and humans; ignored at runtime.

if __name__ == "__main__":
    print("Run directly to observe dynamic typing behavior.")
