# Sets and frozensets are two built-in collection data types in Python. Both are used to store unique elements,
#  but they differ in one major aspect: mutability.


# Both set and frozenset are built-in Python collection data types used to store unique elements.

numbers = {1, 2, 3, 4, 5}

# Adding elements
numbers.add(6)

# Removing elements
numbers.remove(2)

# Updating elements
numbers.update([7, 8, 9])

print(numbers)


"""
Set Methods:

add()
    Adds one element to the set.

update()
    Adds multiple elements to the set.

remove()
    Removes an element from the set.
    Raises KeyError if the element does not exist.

discard()
    Removes an element from the set.
    Does not raise an error if the element does not exist.

pop()
    Removes and returns an arbitrary element from the set.

clear()
    Removes all elements from the set.

union()
    Returns a new set containing all elements from both sets.

intersection()
    Returns a new set containing only the common elements.

difference()
    Returns a new set containing elements present in the first set
    but not in the other set.

symmetric_difference()
    Returns a new set containing elements present in either set,
    but not in both sets.
"""


# ==============================================================================
# SET METHODS IN PYTHON
# ==============================================================================

# Creating sets
A = {10, 20, 30, 40, 50}
B = {40, 50, 60, 70, 80}

print("Original Set A:", A)
print("Original Set B:", B)


# ------------------------------------------------------------------------------
# 1. add()
# Adds one element to the set.
# ------------------------------------------------------------------------------

A.add(60)
print("\n1. add():", A)


# ------------------------------------------------------------------------------
# 2. update()
# Adds multiple elements to the set.
# ------------------------------------------------------------------------------

A.update([70, 80, 90])
print("2. update():", A)


# ------------------------------------------------------------------------------
# 3. remove()
# Removes an element. Raises KeyError if the element does not exist.
# ------------------------------------------------------------------------------

A.remove(90)
print("3. remove():", A)


# ------------------------------------------------------------------------------
# 4. discard()
# Removes an element. Does not raise an error if the element does not exist.
# ------------------------------------------------------------------------------

A.discard(100)
print("4. discard():", A)


# ------------------------------------------------------------------------------
# 5. pop()
# Removes and returns an arbitrary element from the set.
# ------------------------------------------------------------------------------

removed_element = A.pop()
print("5. pop():")
print("Removed Element:", removed_element)
print("Updated Set:", A)


# ------------------------------------------------------------------------------
# 6. clear()
# Removes all elements from the set.
# ------------------------------------------------------------------------------

C = {1, 2, 3, 4, 5}
C.clear()
print("6. clear():", C)


# ------------------------------------------------------------------------------
# 7. union()
# Returns a new set containing all elements from both sets.
# ------------------------------------------------------------------------------

result = A.union(B)
print("7. union():", result)


# ------------------------------------------------------------------------------
# 8. intersection()
# Returns a new set containing only common elements.
# ------------------------------------------------------------------------------

result = A.intersection(B)
print("8. intersection():", result)


# ------------------------------------------------------------------------------
# 9. difference()
# Returns elements present in the first set but not in the second.
# ------------------------------------------------------------------------------

result = A.difference(B)
print("9. difference():", result)


# ------------------------------------------------------------------------------
# 10. symmetric_difference()
# Returns elements present in either set, but not in both.
# ------------------------------------------------------------------------------

result = A.symmetric_difference(B)
print("10. symmetric_difference():", result)


# ==============================================================================
# END OF SET METHODS
# ==============================================================================

# -----------------------------------------------

# Frozenset

numbers = frozenset([1, 2, 3, 4, 5])

print(numbers)
a = frozenset([1, 2, 3])
b = frozenset([3, 4, 5])

print(a.union(b))
print(a.intersection(b))
print(a.difference(b))
print(a.symmetric_difference(b))
