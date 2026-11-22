# Why do we use functions?
# There are several important reasons:
# 1. Code reusability: Write once and execute multiple times.
# 2. Modularity: Divide a large program into smaller components.
# 3. Readability: Make code easier to understand.
# 4. Maintainability: Update logic in one place rather than everywhere.
# 5. Testing: Individual functions can be tested independently.

def divider():
    print("=" * 50)

def greet(name):
    print(f"Hello, {name}!")


greet("Rohit")

divider()

def add_print(a, b):
    print(a + b)


def add_return(a, b):
    return a + b


result1 = add_print(10, 20)
result2 = add_return(10, 20)

print("Result 1:", result1)
print("Result 2:", result2)

divider()


def calculate(a, b, /, *, operation):
    print(a, b, operation)

calculate(10, 20, operation="div")


divider()

def calculate_sum(*args):
    print(args)
    print(sum(args))

calculate_sum(10, 20, 30, 40)


divider()

def user_details(**kwargs):
    print(kwargs)

user_details(name="Rohit", age=17, country="India")