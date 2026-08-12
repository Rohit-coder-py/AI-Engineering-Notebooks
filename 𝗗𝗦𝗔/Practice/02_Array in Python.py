
#how to create a array

from array import array

arr = array('i', [10, 20, 30, 40, 50])

print(arr)

#iteration

for i in range(len(arr)):
    print(arr[i],end = '  ')
    
    
print('\n==================================================\n')
#using enhanced for loop
    
for x in arr:
    print(x,end = ' , ')
    
    
print('\n')   
    
    
    
    
#more operations
    
#how to know typecode of a arr
    
print(arr.typecode)

#slincing

arr = array('i', [10, 20, 30, 40, 50, 60])

print("Original Array :", arr)

print("\nIndexing")

print("First Element       :", arr[0])

print("Third Element       :", arr[2])

print("Last Element        :", arr[-1])

print("Second Last Element :", arr[-2])


#Slicing

print("arr[:]    :", arr[:])
print("arr[1:4]  :", arr[1:4])
print("arr[:3]   :", arr[:3])

print("arr[3:]   :", arr[3:])

print("arr[::2]  :", arr[::2])
print("arr[::-1] :", arr[::-1])
arr[1::2]


#creating array using numpy module


import numpy as np

arr = np.array([10, 20, 30, 40, 50])


for x in arr:
    print(x,end = ' ')
    
print('\n')

for i in range(len(arr)):
    print(arr[i],end = ' ')
    
