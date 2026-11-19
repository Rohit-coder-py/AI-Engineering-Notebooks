"""
12 - INTERVIEW PRACTICAL (SOLVED)
==================================
Part A: Predict the output (answers listed at the bottom as asserts)
Part B: Coding questions with solutions and tests

How to use:
  1. Cover the solution, try yourself first (use 13_interview_practice_BLANK.py)
  2. Compare, then explain TIME & SPACE complexity out loud.

Run: python 12_interview_practical_solved.py   (all asserts should pass)
"""
from collections import Counter, defaultdict

# ======================================================================
# PART A - PREDICT THE OUTPUT
# ======================================================================
# Q1
a = [1, 2, 3]; b = a; b.append(4)
q1 = a                                  # -> [1, 2, 3, 4]     (alias)

# Q2
x = 256; y = 256
q2 = x is y                             # True (small int cache)

# Q3
q3 = 0.1 + 0.2 == 0.3                   # False (float precision)

# Q4
q4 = [] or "fallback"                   # 'fallback'

# Q5
q5 = [1, 2, 3] * 2                      # [1,2,3,1,2,3]

# Q6
def add(item, bucket=[]):
    bucket.append(item)
    return bucket
add(1)
q6 = add(2)                             # [1, 2]  (mutable default shared)

# Q7
q7 = {1: "a", True: "b"}                # {1: 'b'}

# Q8
t = (1, [2, 3]); t[1].append(4)
q8 = t                                  # (1, [2, 3, 4])

# Q9
q9 = -7 // 2, -7 % 2                    # (-4, 1)

# Q10
q10 = "abc"[::-1] + str(1 + 2)          # 'cba3'

# Q11
q11 = [i for i in range(10) if i % 3 == 0]   # [0, 3, 6, 9]

# Q12
funcs = [lambda: i for i in range(3)]
q12 = [f() for f in funcs]              # [2, 2, 2]

# Q13
q13 = len(set("mississippi"))           # 4

# Q14
lst = [3, 1, 2]
q14 = (lst.sort(), lst)                 # (None, [1, 2, 3])

# Q15
for i in range(3):
    pass
q15 = i                                 # 2 (loop var leaks)

# Q16
q16 = 5 and 0 or 7                      # 7

# Q17
s = {1, 2, 3}
q17 = s - {2} | {9}                     # {1, 3, 9}

# Q18
d = dict.fromkeys(range(2), [])
d[0].append("x")
q18 = d                                 # {0: ['x'], 1: ['x']}

assert q1 == [1, 2, 3, 4] and q2 is True and q3 is False
assert q4 == "fallback" and q5 == [1, 2, 3, 1, 2, 3] and q6 == [1, 2]
assert q7 == {1: "b"} and q8 == (1, [2, 3, 4]) and q9 == (-4, 1)
assert q10 == "cba3" and q11 == [0, 3, 6, 9] and q12 == [2, 2, 2]
assert q13 == 4 and q14 == (None, [1, 2, 3]) and q15 == 2 and q16 == 7
assert q17 == {1, 3, 9} and q18 == {0: ["x"], 1: ["x"]}
print("Part A answers verified.")


# ======================================================================
# PART B - CODING QUESTIONS
# ======================================================================
def reverse_string(s):
    """Q1. Reverse a string without [::-1]. O(n)"""
    out = []
    for ch in s:
        out.insert(0, ch)           # O(n) each -> O(n^2); better: iterate reversed
    return "".join(out)

def reverse_string_fast(s):
    return "".join(s[i] for i in range(len(s) - 1, -1, -1))


def is_palindrome(s):
    """Q2. Ignore case & non-alphanumerics. O(n)"""
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]


def count_vowels(s):
    """Q3."""
    return sum(1 for c in s.lower() if c in "aeiou")


def fizzbuzz(n):
    """Q4."""
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0
            else "Buzz" if i % 5 == 0 else str(i) for i in range(1, n + 1)]


def is_prime(n):
    """Q5. O(sqrt n)"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def fibonacci(n):
    """Q6. First n numbers. O(n)"""
    a, b, out = 0, 1, []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out


def factorial(n):
    """Q7."""
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def sum_of_digits(n):
    """Q8."""
    n, total = abs(n), 0
    while n:
        total += n % 10
        n //= 10
    return total


def is_armstrong(n):
    """Q9. 153 = 1^3 + 5^3 + 3^3"""
    digits = str(n)
    return n == sum(int(d) ** len(digits) for d in digits)


def second_largest(nums):
    """Q10. Without sorting whole list. O(n)"""
    first = second = float("-inf")
    for n in nums:
        if n > first:
            first, second = n, first
        elif first > n > second:
            second = n
    return None if second == float("-inf") else second


def remove_duplicates(nums):
    """Q11. Keep order. O(n)"""
    seen, out = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n); out.append(n)
    return out


def two_sum(nums, target):
    """Q12. Return indices. O(n) time, O(n) space"""
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []


def char_frequency(s):
    """Q13."""
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def first_non_repeating(s):
    """Q14. Return the char or None."""
    freq = Counter(s)
    for ch in s:
        if freq[ch] == 1:
            return ch
    return None


def is_anagram(a, b):
    """Q15."""
    return Counter(a.replace(" ", "").lower()) == Counter(b.replace(" ", "").lower())


def group_anagrams(words):
    """Q16."""
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return sorted(sorted(v) for v in g.values())


def rotate_list(nums, k):
    """Q17. Rotate right by k."""
    if not nums:
        return nums
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]


def flatten(nested):
    """Q18. Flatten arbitrarily nested lists (recursion)."""
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def common_elements(a, b):
    """Q19."""
    return sorted(set(a) & set(b))


def missing_number(nums):
    """Q20. nums has n distinct numbers from 0..n, one missing."""
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def word_count(text):
    """Q21. Case-insensitive, ignore punctuation."""
    import string
    cleaned = text.lower().translate(str.maketrans("", "", string.punctuation))
    return dict(Counter(cleaned.split()))


def invert_dict(d):
    """Q22. Values may repeat -> collect keys into lists."""
    out = defaultdict(list)
    for k, v in d.items():
        out[v].append(k)
    return dict(out)


def merge_sorted(a, b):
    """Q23. Two-pointer merge. O(n+m)"""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]


def pair_with_sum(nums, target):
    """Q24. All unique pairs summing to target (values)."""
    seen, pairs = set(), set()
    for n in nums:
        if target - n in seen:
            pairs.add(tuple(sorted((n, target - n))))
        seen.add(n)
    return sorted(pairs)


def max_consecutive_ones(nums):
    """Q25."""
    best = cur = 0
    for n in nums:
        cur = cur + 1 if n == 1 else 0
        best = max(best, cur)
    return best


def transpose(matrix):
    """Q26."""
    return [list(row) for row in zip(*matrix)]


def pascal_row(n):
    """Q27. nth row (0-indexed) of Pascal's triangle."""
    row = [1]
    for _ in range(n):
        row = [a + b for a, b in zip([0] + row, row + [0])]
    return row


def caesar(text, shift):
    """Q28."""
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def gcd(a, b):
    """Q29. Euclid."""
    while b:
        a, b = b, a % b
    return a


def to_binary(n):
    """Q30. Without bin()."""
    if n == 0:
        return "0"
    bits = []
    while n:
        bits.append(str(n % 2))
        n //= 2
    return "".join(reversed(bits))


# ----------------------------- TESTS -----------------------------------
assert reverse_string("hello") == reverse_string_fast("hello") == "olleh"
assert is_palindrome("A man, a plan, a canal: Panama") and not is_palindrome("abc")
assert count_vowels("Python Interview") == 5
assert fizzbuzz(15)[-1] == "FizzBuzz" and fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
assert [n for n in range(20) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19]
assert fibonacci(8) == [0, 1, 1, 2, 3, 5, 8, 13]
assert factorial(5) == 120 and factorial(0) == 1
assert sum_of_digits(-1234) == 10
assert is_armstrong(153) and not is_armstrong(154)
assert second_largest([5, 1, 9, 9, 3]) == 5 and second_largest([2, 2]) is None
assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert char_frequency("aab") == {"a": 2, "b": 1}
assert first_non_repeating("swiss") == "w" and first_non_repeating("aabb") is None
assert is_anagram("Listen", "Silent") and not is_anagram("a", "b")
assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
assert flatten([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5]
assert common_elements([1, 2, 3, 4], [3, 4, 5]) == [3, 4]
assert missing_number([3, 0, 1]) == 2
assert word_count("Hi, hi! Bye.") == {"hi": 2, "bye": 1}
assert invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
assert merge_sorted([1, 4, 7], [2, 3, 9]) == [1, 2, 3, 4, 7, 9]
assert pair_with_sum([1, 2, 3, 4, 5], 6) == [(1, 5), (2, 4)]
assert max_consecutive_ones([1, 1, 0, 1, 1, 1]) == 3
assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert pascal_row(4) == [1, 4, 6, 4, 1]
assert caesar("Abc xyz", 3) == "Def abc"
assert gcd(48, 18) == 6
assert to_binary(10) == "1010" and to_binary(0) == "0"

print("Part B: all 30 coding questions pass.")
print("\nFollow-ups interviewers love:")
print(" - What is the time/space complexity of your solution?")
print(" - Can you do it in one pass / without extra space?")
print(" - What if the input is empty, has None, negative numbers, or huge size?")
