def student_details(**a):
    print(a)

student_details(name="Harsh", age=21, course="Python")

def student_details(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

student_details(name="Harsh", age=21, course="Python")
