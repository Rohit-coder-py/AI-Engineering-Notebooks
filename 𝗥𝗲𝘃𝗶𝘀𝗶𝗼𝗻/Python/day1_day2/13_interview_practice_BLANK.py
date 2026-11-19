"""
13 - INTERVIEW PRACTICE (BLANK - YOUR TURN)
============================================
Implement every function, then run:  python 13_interview_practice_BLANK.py
Tests at the bottom tell you what's passing. Solutions: 12_interview_practical_solved.py
Rules: no peeking for 20 minutes per question. Say the complexity out loud.

Replace `raise NotImplementedError` / `pass` with your code.
"""


def reverse_words(sentence):
    """'the sky is blue' -> 'blue is sky the'. Handle extra spaces."""
    raise NotImplementedError


def is_balanced(s):
    """Check brackets ()[]{} balance using a list as a stack.
    '([]{})' -> True, '(]' -> False, '((' -> False"""
    raise NotImplementedError


def count_words_longer_than(text, n):
    """Return how many words in text have length > n."""
    raise NotImplementedError


def swap_case_manual(s):
    """Swap upper/lower without s.swapcase(). 'aBc' -> 'AbC'"""
    raise NotImplementedError


def most_common_char(s):
    """Return the most frequent character (ties: the one appearing first)."""
    raise NotImplementedError


def list_to_dict_by_length(words):
    """['hi', 'yo', 'hey'] -> {2: ['hi', 'yo'], 3: ['hey']}"""
    raise NotImplementedError


def intersection_no_set(a, b):
    """Common elements of two lists WITHOUT using set(). Keep order of a, no duplicates."""
    raise NotImplementedError


def second_smallest(nums):
    """Second smallest DISTINCT value or None."""
    raise NotImplementedError


def move_zeros_to_end(nums):
    """[0,1,0,3,12] -> [1,3,12,0,0] keeping order of non-zeros."""
    raise NotImplementedError


def is_sorted(nums):
    """True if non-decreasing. Single pass."""
    raise NotImplementedError


def chunk_list(nums, size):
    """chunk_list([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]"""
    raise NotImplementedError


def dict_from_two_lists(keys, values):
    """Build dict without dict(zip()). Extra keys get None; extra values ignored."""
    raise NotImplementedError


def remove_vowels(s):
    """'Interview' -> 'ntrvw'"""
    raise NotImplementedError


def longest_word(sentence):
    """Return the longest word (first one on ties)."""
    raise NotImplementedError


def digits_to_number(digits):
    """[1, 2, 3] -> 123 without str() / int()."""
    raise NotImplementedError


def count_pairs_with_diff(nums, k):
    """Count UNIQUE pairs (a, b) from nums with a - b == k (k > 0). Use a set."""
    raise NotImplementedError


def spiral_or_pattern(n):
    """Return list of strings forming a right-angled number triangle:
    n=3 -> ['1', '12', '123']"""
    raise NotImplementedError


def validate_username(name):
    """Valid if: 4-12 chars, starts with a letter, only letters/digits/underscore."""
    raise NotImplementedError


def merge_dicts_sum(d1, d2):
    """Merge dicts; for common keys add values. {'a':1,'b':2} + {'b':3} -> {'a':1,'b':5}"""
    raise NotImplementedError


def explain_in_comments():
    """Write answers as comments below, then return True.
    1) Why is list.pop(0) O(n)?
    2) Why can't a list be a dict key?
    3) What does 'x is y' compare?
    """
    # 1)
    # 2)
    # 3)
    return True


# ======================================================================
# TESTS - don't edit below this line
# ======================================================================
def run_tests():
    tests = [
        ("reverse_words", lambda: reverse_words("  the sky  is blue ") == "blue is sky the"),
        ("is_balanced", lambda: is_balanced("([]{})") and not is_balanced("(]") and not is_balanced("((")),
        ("count_words_longer_than", lambda: count_words_longer_than("a quick brown fox", 3) == 2),
        ("swap_case_manual", lambda: swap_case_manual("aBc1") == "AbC1"),
        ("most_common_char", lambda: most_common_char("abbcc") == "b"),
        ("list_to_dict_by_length", lambda: list_to_dict_by_length(["hi", "yo", "hey"]) == {2: ["hi", "yo"], 3: ["hey"]}),
        ("intersection_no_set", lambda: intersection_no_set([1, 2, 2, 3], [2, 3, 4]) == [2, 3]),
        ("second_smallest", lambda: second_smallest([4, 1, 1, 3]) == 3 and second_smallest([1, 1]) is None),
        ("move_zeros_to_end", lambda: move_zeros_to_end([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]),
        ("is_sorted", lambda: is_sorted([1, 2, 2, 5]) and not is_sorted([2, 1])),
        ("chunk_list", lambda: chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]),
        ("dict_from_two_lists", lambda: dict_from_two_lists(["a", "b", "c"], [1, 2]) == {"a": 1, "b": 2, "c": None}),
        ("remove_vowels", lambda: remove_vowels("Interview") == "ntrvw"),
        ("longest_word", lambda: longest_word("I love programming daily") == "programming"),
        ("digits_to_number", lambda: digits_to_number([1, 2, 3]) == 123),
        ("count_pairs_with_diff", lambda: count_pairs_with_diff([1, 5, 3, 4, 2], 2) == 3),
        ("spiral_or_pattern", lambda: spiral_or_pattern(3) == ["1", "12", "123"]),
        ("validate_username", lambda: validate_username("harsh_01") and not validate_username("1abc") and not validate_username("ab")),
        ("merge_dicts_sum", lambda: merge_dicts_sum({"a": 1, "b": 2}, {"b": 3}) == {"a": 1, "b": 5}),
        ("explain_in_comments", lambda: explain_in_comments() is True),
    ]
    passed = 0
    for name, check in tests:
        try:
            ok = bool(check())
        except NotImplementedError:
            ok = None
        except Exception as e:  # noqa
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
            ok = False
        status = {True: "PASS", False: "FAIL", None: "TODO"}[ok]
        print(f"[{status}] {name}")
        passed += ok is True
    print(f"\n{passed}/{len(tests)} passed")


if __name__ == "__main__":
    run_tests()
