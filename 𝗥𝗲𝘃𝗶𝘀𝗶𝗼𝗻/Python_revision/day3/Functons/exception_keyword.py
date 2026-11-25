try:
    num = int(input("Enter a number: "))
    result = 10 / num
    print(result)

except ValueError:
    print("Invalid input")

except ZeroDivisionError:
    print("Cannot divide by zero")

finally:
    print("Execution completed")
    
    
    
    
print(num)