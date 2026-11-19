"""
================================================================================
PROJECT 1 — Simple Calculator
Concepts used (Day 1): variables, assignment, dynamic typing, type conversion,
arithmetic/comparison/logical operators, truthiness, conditionals (Day 2).
================================================================================
"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def get_number(prompt):
    """Prompt user until a valid number is entered. Uses type conversion."""
    while True:
        raw = input(prompt)
        try:
            # Prefer int when possible, else float
            if "." in raw:
                return float(raw)
            return int(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def main():
    print("=== Simple Calculator ===")
    print("Operations: +  -  *  /")
    print("Type 'q' to quit\n")

    while True:
        choice = input("Choose operation (+, -, *, /) or 'q' to quit: ").strip()

        if choice == "q":
            print("Goodbye!")
            break

        if choice not in {"+", "-", "*", "/"}:
            print("Invalid operation. Try again.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            if choice == "+":
                result = add(a, b)
            elif choice == "-":
                result = subtract(a, b)
            elif choice == "*":
                result = multiply(a, b)
            else:
                result = divide(a, b)

            # Dynamic typing in action: result may be int or float
            print(f"Result: {a} {choice} {b} = {result}\n")

        except ValueError as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
