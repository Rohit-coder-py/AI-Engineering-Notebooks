"""
================================================================================
PROJECT 4 — Password Validator
Concepts used (Day 1 + Day 2): strings (iterable), loops, conditionals,
membership operators, logical operators, truthiness, type conversion (len),
break/continue, boolean flags.
================================================================================
"""

def validate_password(password):
    """
    Validate a password against these rules:
      - at least 8 characters
      - at least one uppercase letter
      - at least one lowercase letter
      - at least one digit
      - at least one special character
    Returns (is_valid: bool, messages: list of str)
    """
    errors = []

    if len(password) < 8:
        errors.append("At least 8 characters long")

    has_upper = any(ch.isupper() for ch in password)   # generator + any()
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)

    specials = set("!@#$%^&*()-_=+[]{}|;:,.<>?/")
    has_special = any(ch in specials for ch in password)   # membership in set

    if not has_upper:
        errors.append("At least one uppercase letter (A-Z)")
    if not has_lower:
        errors.append("At least one lowercase letter (a-z)")
    if not has_digit:
        errors.append("At least one digit (0-9)")
    if not has_special:
        errors.append("At least one special character (!@#$%^&*...)")

    return (len(errors) == 0), errors


def main():
    print("=== Password Validator ===")
    print("Rules: 8+ chars, uppercase, lowercase, digit, special character.\n")

    while True:
        password = input("Enter password (or 'q' to quit): ").strip()

        if password == "q":
            print("Goodbye!")
            break

        if not password:              # truthiness check for empty input
            print("Password cannot be empty.\n")
            continue

        valid, errors = validate_password(password)

        if valid:
            print("✓ Password is strong and valid!\n")
            break
        else:
            print("✗ Password is weak. Missing:")
            for err in errors:
                print(f"   - {err}")
            print("Try again.\n")


if __name__ == "__main__":
    main()
