#simple algorithm

x = 5
print(x)

# Time complexity type

#1.Constant Time - O(1)            (y = 5)

x = 5
print(x)

# 2. Linear Time - O(n)     (y = 2x + 5)

n = 5

for i in range(n):
    print(i)
    
    
#Quadratic Time  - O(n²)          (y = 2x² + 2n + 5)
    
    
arr = [10, 20, 30, 40, 50]

for i in range(len(arr)):
    for j in range(len(arr)):
        print(arr[i], arr[j])
        
analysis = """
Outer loop = n

Inner loop = n

Total operations = n × n

= n²

Time Complexity = O(n²)
"""




# 3. Cubic Time - O(n³)     (y = x³ + x² + x + 2)

arr = [10, 20, 30, 40, 50]

for i in range(len(arr)):
    for j in range(len(arr)):
        for k in range(len(arr)):
            print(arr[i], arr[j], arr[k])


'''

x = Total number of operations

1 + 1 + n + n² + n³

= n³ + n² + n + 2

Dominating Factor = n³

Time Complexity = O(n³)
'''

    
## Logarithmic Time Complexity -  O(logn)   2logn+2


n = 10 

while n >= 1:
    print("Hello")
    n = n // 2
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# =================================================================================================================
                              #* PRACTICE *
#=================================================================================================================


#Q: Find time complexities ? 


# Q1
n = 10
print(n)
print(n + 5)

#Ans : O(1)


# Q2
n = 10

for i in range(n):
    print(i)
#Ans : O(n)


# Q3
n = 10

for i in range(n):
    print(i)

for j in range(n):
    print(j)

#Ans : O(n)

# Q4
n = 10

for i in range(n):
    for j in range(n):
        print(i, j)
#Ans : O(n2)

# Q5
n = 10

for i in range(n):
    for j in range(n):
        for k in range(n):
            print(i, j, k)

#Ans : O(n3)

# Q6
n = 10

for i in range(n):
    print(i)

for j in range(n):
    for k in range(n):
        print(j, k)

#Ans : O(n2)

# Q7
n = 64

while n >= 1:
    print(n)
    n = n // 2
#Ans : O(logn)


# Q8
n = 10

for i in range(n):
    print(i)

for j in range(n):
    for k in range(n):
        print(j, k)

while n >= 1:
    n = n // 2
    
#Ans : O(n2) because in order 0(n2) is dominating
    
    
    
# Result : All correct 
