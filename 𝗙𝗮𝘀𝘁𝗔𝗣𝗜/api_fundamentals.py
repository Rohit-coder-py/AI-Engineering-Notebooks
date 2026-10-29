from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "welcome to homepage start shopping here "}



#we use Pydantic when we need to send / use post

from pydantic import BaseModel
from typing import List,Optional



class User(BaseModel):
    user_id : int
    user_name: str
    user_ph :int
    user_loc: str



@app.post("/userprofile")
def user_profile(profile: User):
    return {"message": "User profile received successfully",
            "user": profile}


users = {
    1: {"user_name": "Rahul", "user_ph": 9876543210, "user_loc": "Lucknow"},  #id : 1
    2: {"user_name": "Aman", "user_ph": 9876543211, "user_loc": "Delhi"},
    3: {"user_name": "Priya", "user_ph": 9876543212, "user_loc": "Mumbai"}
}


#paths

@app.get("/user/{user_id}")
def get_user(user_id: int):
    
    if user_id not in users:
        return {"error": f"User {user_id} not found"}

    return {
        "user_id": user_id,
        **users[user_id]
        }


#multiple paths url


@app.get("/model/{model_name}/user/{user_id}")
def get_model_prediction(model_name: str, user_id: int):
    return {
        "model": model_name,
        "user_id": user_id,
        "prediction": "High Risk"
    }



#apply conditions on path



