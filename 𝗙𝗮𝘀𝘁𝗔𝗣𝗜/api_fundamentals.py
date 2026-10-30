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


# Query Parameters

@app.get("/usersfilter")
def get_customer(
    user_name: Optional[str] = None,
    user_loc: Optional[str] = None
):
    filtered_users = {}

    for user_id, user_data in users.items():

        # Filter by username
        if user_name and user_name.lower() not in user_data["user_name"].lower():
            continue

        # Filter by location
        if user_loc and user_loc.lower() != user_data["user_loc"].lower():
            continue

        filtered_users[user_id] = user_data

    return {
        "total_users": len(filtered_users),
        "users": filtered_users
    }

# You can control the number of records returned using Query Parameters: limit and skip.
        