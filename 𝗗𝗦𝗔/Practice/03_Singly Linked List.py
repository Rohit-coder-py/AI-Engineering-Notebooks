# Step 1: Create a Node class
# 
# Each node stores:
# 
# data
# next

class Node:
    def __init__(self, data):
        self.data = data      # Store the value
        self.next = None      # Initially points to nothing


#Step 2 :Create nodes(they have no conncetion between them )
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)
node4 = Node(40)

#Step 3 : Connect the nodes
node1.next = node2
node2.next = node3
node3.next = node4

# Head of the linked list
head = node1

#Step 5: Traverse (Print the List)

current = head

while current is not None:
    print(current.data, end=" -> ")
    current = current.next

print("None")

#memory allocation
# x = 10
# 
# print(id(x))
# 
# 
# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.next = None
# 
# node1 = Node(10)
# node2 = Node(20)
# 
# print(id(node1))
# print(id(node2))


print(head.data)
print(head.data)
print(head.next)



print(head.data)                 # 10
print(head.next.data)            # 20
print(head.next.next.data)       # 30
print(head.next.next.next.data)  # 40
print(head.next.next.next.data)  # 40


print(head.next.data)                 

print(node1.data)

print(19-12)