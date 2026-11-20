# t = "pythoc"
# 
# t[-1] = 'n'
# 
# print(t)


name = "PYTHON"

new_name = name.replace("P", "J")

print(new_name)
print(name)


name = "PYTHON"

new_name = "J" + name[1:]

print(new_name)


first_name = "Rohit"
last_name = "Jha"

full_name = first_name + " " + last_name

print(full_name)



a = "Python"
b = "is"
c = "awesome"

result = a + " " + b + " " + c

print(result)


age = 17
message = "My age is " + str(age)

print(message)


text = "Python"

result = text * 3

print(result)

symbol = "*"

print(symbol * 10)


print("Python" * 5)
print("Python" * -2)


name = "Rohit"
separator = "-"

print(name + separator * 5 + "Python")

print()
print()
print()
print()



#Formattings

name = "Rohit"
age = 17

message = f"My name is {name} and I am {age} years old."

print(message)


a = 10
b = 20

print(f"Sum = {a + b}")
print(f"Product = {a * b}")
print(f"Division = {b / a}")


name = "rohit"

print(f"Name: {name.upper()}")


#formtted decimals


price = 123.45678

print(f"Price: {price:.2f}")


pi = 3.14159265

print(f"{pi:.2f}")
print(f"{pi:.3f}")
print(f"{pi:.4f}")


amount = 1000000

print(f"Amount: {amount:,}")

print()
print()
print()
print()


name = "Python"

print(f"{name:>8}")
print(f"{name:<15}")
print(f"{name:^15}")



#project

name = "Rohit"
course = "BCA"
marks = 87.456

report = f"""
Student Report
--------------
Name: {name}
Course: {course}
Marks: {marks:.2f}
"""

print(report)


#format()

name = "Rohit"
age = 17

message = "My name is {} and I am {} years old.".format(name, age)

print(message)


name = "Rohit"
language = "Python"

print("{0} is learning {1}".format(name, language))
print("{1} is being learned by {0}".format(name, language))



# %

name = "Rohit"
age = 17

print("My name is %s and I am %d years old." % (name, age))

# %s - str
# 
# %d = int
# 
# %f = float 
# 
# %.2f = decimal precised


text = "Python Programming"

print("Python" in text)       # True
print("Java" in text)         # False

print("Java" not in text)     # True
print("Python" not in text)   # False
# Important: Membership checks are case-sensitive



email = "user@gmail.com"

if "@gmail.com" in email:
    print("Gmail address detected")
    
    
    
#-----------ord() and chr()
    
print(ord("A"))  # 65
print(ord("a"))  # 97
print(ord("₹"))  # 8377

print("\u0041")       # A
print("\u20B9")       # ₹
print("\U0001F60A")   # 😊

print(chr(66))
