#error handling in fastapi


from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def welcome():
    return{"message" : "Welcome to app "}

@app.post("/register")
def register_user():
    return {
        "message": "User registered successfully",
        "user_data": user
    }
