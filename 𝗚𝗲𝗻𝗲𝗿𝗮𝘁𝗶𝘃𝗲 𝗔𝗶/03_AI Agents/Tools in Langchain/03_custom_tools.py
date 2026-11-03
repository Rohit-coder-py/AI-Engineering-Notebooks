from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:   #what to return
    """Multiply two numbers and return the result."""
    return a * b

#execute the tool
response = multiply.invoke({
    "a": 10,
    "b": 20})

print(response)
print(multiply.name)
print(multiply.description)
print(multiply.args)
print("\n=======")


