"""
============================================================
PYTHON STRINGS: COMMON STRING METHODS
============================================================

A string is an immutable sequence of characters.

IMMUTABILITY:
- String methods do not modify the original string.
- Methods that transform a string return a NEW string.
- If you want to keep the changed result, assign it to a variable.

Run this file to see each method in action.
"""

# ============================================================
# 1. lower()
# ============================================================
# THEORY:
# lower() returns a new string in which all uppercase letters
# are converted to lowercase.
#
# Syntax:
# string.lower()

text = "PyThOn Is FuN"
print("lower():", text.lower())          # python is fun


# ============================================================
# 2. upper()
# ============================================================
# THEORY:
# upper() returns a new string in which all lowercase letters
# are converted to uppercase.
#
# Syntax:
# string.upper()

text = "Python is fun"
print("upper():", text.upper())          # PYTHON IS FUN


# ============================================================
# 3. title()
# ============================================================
# THEORY:
# title() converts the first character of each word to uppercase
# and the remaining characters of each word to lowercase.
#
# Syntax:
# string.title()

text = "learn python programming"
print("title():", text.title())          # Learn Python Programming


# ============================================================
# 4. strip()
# ============================================================
# THEORY:
# strip() removes whitespace from BOTH ends of a string.
# It does not remove whitespace from between words.
#
# You can also pass specific characters to remove from both ends.
#
# Related methods:
# lstrip() -> removes from the left side
# rstrip() -> removes from the right side
#
# Syntax:
# string.strip()
# string.strip(chars)

text = "   Hello Python!   "
print("strip():", repr(text.strip()))

text = "---Python---"
print("strip('-'):", text.strip("-"))


# ============================================================
# 5. split()
# ============================================================
# THEORY:
# split() breaks a string into a list of smaller strings.
# By default, it splits wherever whitespace occurs.
#
# You can provide a separator to decide where to split.
# maxsplit limits the number of splits.
#
# Syntax:
# string.split()
# string.split(separator)
# string.split(separator, maxsplit)

text = "Python is easy to learn"
print("split():", text.split())

text = "apple,banana,mango"
print("split(','):", text.split(","))

text = "one-two-three-four"
print("split('-', 2):", text.split("-", 2))


# ============================================================
# 6. join()
# ============================================================
# THEORY:
# join() combines the elements of an iterable of strings into
# one string, placing the chosen separator between the elements.
#
# The separator is the string on which join() is called.
#
# Syntax:
# separator.join(iterable)
#
# Important: the iterable's elements must be strings.

words = ["Python", "is", "powerful"]
print("join with space():", " ".join(words))
print("join with hyphen:", "-".join(words))
print("join with empty string:", "".join(words))


# ============================================================
# 7. replace()
# ============================================================
# THEORY:
# replace() returns a new string in which occurrences of an old
# substring are replaced with a new substring.
#
# count is optional. It limits how many occurrences are replaced.
#
# Syntax:
# string.replace(old, new)
# string.replace(old, new, count)

text = "I like Java. Java is popular."
print("replace():", text.replace("Java", "Python"))

text = "red red red blue"
print("replace with count:", text.replace("red", "green", 2))


# ============================================================
# 8. find()
# ============================================================
# THEORY:
# find() returns the index of the FIRST occurrence of a substring.
# If the substring is not found, it returns -1.
#
# Indexing starts at 0.
# Optional start and end arguments limit the search range.
#
# Syntax:
# string.find(substring)
# string.find(substring, start, end)

text = "Python programming"
print("find('pro'):", text.find("pro"))
print("find('Java'):", text.find("Java"))    # -1
print("find('o', 5):", text.find("o", 5))


# ============================================================
# 9. index()
# ============================================================
# THEORY:
# index() works like find(): it returns the index of the first
# occurrence of a substring.
#
# IMPORTANT DIFFERENCE:
# - find() returns -1 if the substring is missing.
# - index() raises a ValueError if the substring is missing.
#
# Syntax:
# string.index(substring)
# string.index(substring, start, end)

text = "Python programming"
print("index('pro'):", text.index("pro"))

# Uncomment the next line to see the ValueError:
# print(text.index("Java"))


# ============================================================
# 10. count()
# ============================================================
# THEORY:
# count() returns the number of non-overlapping occurrences of
# a substring in a string.
#
# Optional start and end arguments limit the counting range.
#
# Syntax:
# string.count(substring)
# string.count(substring, start, end)

text = "banana"
print("count('a'):", text.count("a"))
print("count('an'):", text.count("an"))
print("count('a', 2, 5):", text.count("a", 2, 5))


# ============================================================
# 11. startswith()
# ============================================================
# THEORY:
# startswith() checks whether a string begins with a specified
# substring. It returns True or False.
#
# Optional start and end arguments limit the portion checked.
#
# Syntax:
# string.startswith(prefix)
# string.startswith(prefix, start, end)
#
# You can also pass a tuple of prefixes.

text = "Python programming"
print("startswith('Python'):", text.startswith("Python"))
print("startswith('Java'):", text.startswith("Java"))
print("startswith(('Py', 'Ja')):", text.startswith(("Py", "Ja")))


# ============================================================
# 12. endswith()
# ============================================================
# THEORY:
# endswith() checks whether a string ends with a specified
# substring. It returns True or False.
#
# Optional start and end arguments limit the portion checked.
#
# Syntax:
# string.endswith(suffix)
# string.endswith(suffix, start, end)
#
# You can also pass a tuple of suffixes.

filename = "notes.py"
print("endswith('.py'):", filename.endswith(".py"))
print("endswith('.txt'):", filename.endswith(".txt"))
print("endswith(('.py', '.ipynb')):", filename.endswith((".py", ".ipynb")))


# ============================================================
# QUICK REVISION
# ============================================================
# lower()       -> converts letters to lowercase
# upper()       -> converts letters to uppercase
# title()       -> capitalizes the beginning of each word
# strip()       -> removes whitespace (or chosen characters) at both ends
# split()       -> breaks a string into a list
# join()        -> combines strings using a separator
# replace()     -> replaces one substring with another
# find()        -> returns an index, or -1 if not found
# index()       -> returns an index, or raises ValueError if not found
# count()       -> counts non-overlapping occurrences
# startswith()  -> checks the beginning of a string
# endswith()    -> checks the ending of a string


# ============================================================
# PRACTICE TASKS
# ============================================================
# Try these yourself without looking up the answers:
#
# 1. Convert "hello WORLD" entirely to lowercase.
# 2. Convert "python programming" entirely to uppercase.
# 3. Convert "learn python every day" into title case.
# 4. Remove extra spaces from "   learn Python   ".
# 5. Split "red,green,blue" using the comma separator.
# 6. Join ["I", "love", "Python"] using a space.
# 7. Replace "bad" with "good" in "Python is bad".
# 8. Find the index of "code" in "I love coding".
# 9. Count how many times "a" appears in "banana".
# 10. Check whether "machine learning" starts with "machine".
# 11. Check whether "program.py" ends with ".py".
# 12. Explain the difference between find() and index().

