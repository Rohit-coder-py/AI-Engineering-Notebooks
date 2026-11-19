"""
PROJECT 8 (BLANK) - Pattern Printer & Number Utilities (loops practice)
========================================================================
Use ONLY loops + conditionals + string multiplication. Each function must
RETURN a list of strings (one per row), not print directly, so it can be tested.

PATTERNS  (n = 4)
 1. right_triangle(4)       2. pyramid(4)            3. diamond(3)
    *                          "   *"                   "  *"
    **                         "  ***"                  " ***"
    ***                        " *****"                 "*****"
    ****                       "*******"                " ***"
                                                        "  *"
 4. number_triangle(4)      5. hollow_square(4)      6. floyd(4)
    1                          ****                     1
    12                         *  *                     2 3
    123                        *  *                     4 5 6
    1234                       ****                     7 8 9 10

NUMBER UTILITIES (use while / for loops, no math library)
 7. is_prime(n)             8. primes_upto(n)        9. gcd(a, b)  (Euclid)
10. collatz_steps(n)       11. is_perfect(n)        12. digital_root(n)
    steps to reach 1           6 = 1+2+3                9875 -> 29 -> 11 -> 2

BONUS
- multiplication_table(n, up_to=10) returning formatted rows
- a menu in main() that lets the user choose a pattern and size
"""


def right_triangle(n):
    # TODO
    pass


def pyramid(n):
    # TODO
    pass


def diamond(n):
    # TODO
    pass


def number_triangle(n):
    # TODO
    pass


def hollow_square(n):
    # TODO
    pass


def floyd(n):
    # TODO
    pass


def is_prime(n):
    # TODO
    pass


def primes_upto(n):
    # TODO
    pass


def gcd(a, b):
    # TODO
    pass


def collatz_steps(n):
    # TODO
    pass


def is_perfect(n):
    # TODO
    pass


def digital_root(n):
    # TODO
    pass


if __name__ == "__main__":
    for row in pyramid(4):
        print(row)
    # Self-tests (uncomment when ready):
    # assert right_triangle(3) == ["*", "**", "***"]
    # assert pyramid(2) == [" *", "***"]
    # assert diamond(2) == [" *", "***", " *"]
    # assert number_triangle(3) == ["1", "12", "123"]
    # assert hollow_square(3) == ["***", "* *", "***"]
    # assert floyd(3) == ["1", "2 3", "4 5 6"]
    # assert primes_upto(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    # assert gcd(48, 18) == 6 and collatz_steps(6) == 8
    # assert is_perfect(28) and not is_perfect(12)
    # assert digital_root(9875) == 2
