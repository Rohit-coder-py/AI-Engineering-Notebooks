x = 10
print(x)  # 10

x = "Hello"
print(x)  # Hello

x = 3.14
print(x)  # 3.14


# Strong Typing vs Weak Typing


# Strong typing means a programming language enforces type compatibility
#  and doesn't automatically convert unrelated types just to make an operation work.


# Weak typing generally means a language allows more
# implicit type conversions between different types.
#
x = "5"
y = "2"

print(x + y)  # TypeError


# # Static Typing vs Dynamic Typing in Programming

# # Static Typing and Dynamic Typing describe when a programming language checks
# #  types and whether a variable can reference values of different types.

# int x = 10;

# x = 20;       // Valid
# x = "Hello";  // Error


# Explanation:
# - int x = 10 declares x as an integer variable.
# - x = 20 is valid because 20 is an integer.
# - x = "Hello" is invalid because x expects an integer, not a string.
# Examples of statically typed languages include Java, C, C++, and Rust.
# 2. Dynamic Typing
# Dynamic Typing means that types are checked at runtime (during program execution), and variables can reference objects of different types.

# Example (Python):
x = 10
x = 20
x = "Hello"
x = 3.14


# Explanation:

# Python allows x to reference an integer, then a string, and finally a float without requiring an explicit type declaration.

# Examples include Python, JavaScript, and Ruby.
