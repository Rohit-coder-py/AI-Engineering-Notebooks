# Binary Search works only on sorted data

def find_city(cities, target):

    left = 0
    right = len(cities) - 1

    while left <= right:

        middle = (left + right) // 2

        if cities[middle] == target:
            return middle

        elif cities[middle] < target:
            left = middle + 1

        else:
            right = middle - 1

    return -1


cities = [
    "New York", "London", "Paris", "Tokyo", "Delhi", "Mumbai",
    "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune",
    "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Surat",
    "Nagpur", "Indore", "Bhopal", "Patna", "Varanasi",
    "Agra", "Noida", "Gurugram", "Chandigarh", "Amritsar",
    "Srinagar", "Shimla", "Dehradun", "Goa", "Kochi",
    "Thiruvananthapuram", "Bhubaneswar", "Ranchi",
    "Guwahati", "Visakhapatnam", "Mysuru", "Jodhpur",
    "Udaipur", "Dubai"
]

cities.sort()

target_city = "New York"

print(find_city(cities, target_city))



print(cities[26])