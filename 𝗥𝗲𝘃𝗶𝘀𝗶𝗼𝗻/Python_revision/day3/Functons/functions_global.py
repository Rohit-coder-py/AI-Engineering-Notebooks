x = 100

def my_function():
    global x
    x= 50
    print(x)

update()
my_function()
print(x)