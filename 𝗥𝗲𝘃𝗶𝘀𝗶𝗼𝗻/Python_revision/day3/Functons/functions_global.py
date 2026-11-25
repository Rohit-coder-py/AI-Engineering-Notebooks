x = 100

def my_function():
    global x
    x= 50
    print(x)

my_function()
print(x)