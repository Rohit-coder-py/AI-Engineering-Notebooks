from pydantic import BaseModel,ConfigDict
from typing import List,Optional

from datetime import datetime



class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    createdAt: datetime
    address: Address
    tags: List[str] = []

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')} #to encode time and date
    )

# create a user instance
user = User(
    id= 1,
    name= "hitesh",
    email= "hitesh@hc.com",
    createdAt = datetime(2024, 3, 15, 14, 30),
    address= Address(
        street = "something",
        city = "Jaipur",
        zip_code = "001144"
    ),
    is_active = False,
    tags = ["premium", "regular"],
)


#using model.dump() -> provids dict

data = user.model_dump()

print(data)

#uisng model_dump_json() -> provide json string
print("\n\n\n")
data = user.model_dump_json()

print(data)