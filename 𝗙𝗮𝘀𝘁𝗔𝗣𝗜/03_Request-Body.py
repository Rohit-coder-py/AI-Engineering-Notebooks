#pydantic with fastapi

from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI


app = FastAPI()

#Define the request body structure
class User(BaseModel):
    user_id: int
    user_name: str
    user_age: int
    user_city: str


@app.get("/")
def welcome():
    return{"message" : "Welcome to app "}

@app.post("/register")
def register_user(user: User):
    return {
        "message": "User registered successfully",
        "user_data": user
    }


#tip : never trust pydantic validated data always apply fields on the important datas 