
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
