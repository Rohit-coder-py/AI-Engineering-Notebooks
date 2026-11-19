"""
PROJECT 5 (BLANK) - Password Strength Checker
==============================================
Concepts to practice: strings, loops, conditionals, sets, any/all, functions.

REQUIREMENTS
1. check_password(pw) returns a dict:
      {"valid": bool, "score": int (0-5), "problems": [list of strings]}
2. Rules (each satisfied rule = 1 point):
      - length >= 8
      - has an uppercase letter
      - has a lowercase letter
      - has a digit
      - has a special char from  !@#$%^&*()-_
   "valid" only if ALL rules pass AND password is not in COMMON_PASSWORDS.
3. Reject passwords containing 3 identical chars in a row (e.g. 'aaa').
4. strength_label(score): 0-2 'Weak', 3-4 'Medium', 5 'Strong'
5. main(): loop asking for a password until valid or the user types 'quit'.
   Print problems each time.

HINTS
- str.isupper(), str.islower(), str.isdigit(), `in`
- any(c.isdigit() for c in pw)
- use a set for SPECIAL and COMMON_PASSWORDS

BONUS
- Count how many attempts the user needed
- Write a generate_password(length) using the random module
"""

SPECIAL = set("!@#$%^&*()-_")
COMMON_PASSWORDS = {"password", "12345678", "qwerty123", "admin123"}


def check_password(pw):
    # TODO
    pass


def strength_label(score):
    # TODO
    pass


def main():
    # TODO
    pass


if __name__ == "__main__":
    main()
    # Quick self-tests (uncomment when ready):
    # assert check_password("Abcdef1!")["valid"] is True
    # assert check_password("abc")["valid"] is False
    # assert check_password("Passsword1!")["valid"] is False   # 'sss'
    # assert strength_label(5) == "Strong" and strength_label(1) == "Weak"
