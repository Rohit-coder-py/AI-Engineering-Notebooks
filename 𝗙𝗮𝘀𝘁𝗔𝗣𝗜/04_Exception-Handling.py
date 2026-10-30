#error handling in fastapi


from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def welcome():
    return{"message" : "Welcome to app "}

#dataset
students = {
    101: {
        "name": "Aarav Sharma",
        "age": 20,
        "gender": "Male",
        "city": "Delhi",
        "course": "BCA",
        "marks": 85,
        "grade": "A"
    },
    102: {
        "name": "Priya Verma",
        "age": 19,
        "gender": "Female",
        "city": "Lucknow",
        "course": "BTech",
        "marks": 92,
        "grade": "A+"
    },
    103: {
        "name": "Rahul Singh",
        "age": 21,
        "gender": "Male",
        "city": "Mumbai",
        "course": "BCA",
        "marks": 67,
        "grade": "B"
    },
    104: {
        "name": "Ananya Gupta",
        "age": 20,
        "gender": "Female",
        "city": "Jaipur",
        "course": "BSc",
        "marks": 78,
        "grade": "B+"
    },
    105: {
        "name": "Vikram Patel",
        "age": 22,
        "gender": "Male",
        "city": "Ahmedabad",
        "course": "BTech",
        "marks": 56,
        "grade": "C"
    },
    106: {
        "name": "Sneha Mishra",
        "age": 19,
        "gender": "Female",
        "city": "Kanpur",
        "course": "BCA",
        "marks": 95,
        "grade": "A+"
    },
    107: {
        "name": "Arjun Yadav",
        "age": 21,
        "gender": "Male",
        "city": "Bhopal",
        "course": "BBA",
        "marks": 72,
        "grade": "B"
    },
    108: {
        "name": "Kavya Joshi",
        "age": 20,
        "gender": "Female",
        "city": "Pune",
        "course": "BSc",
        "marks": 88,
        "grade": "A"
    },
    109: {
        "name": "Rohan Kumar",
        "age": 23,
        "gender": "Male",
        "city": "Patna",
        "course": "BCA",
        "marks": 45,
        "grade": "D"
    },
    110: {
        "name": "Meera Kapoor",
        "age": 19,
        "gender": "Female",
        "city": "Chandigarh",
        "course": "BTech",
        "marks": 81,
        "grade": "A"
    }
}


#now exception handling

from fastapi import HTTPException



# Exception Handling
@app.get("/students/{student_id}")
def student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )

    return students[student_id]



#we can use multiple httpexception in one program

#httpexception is onl u sed for fastapi whiule handling different librares use try-except