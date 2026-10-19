import pydantic
from pydantic import BaseModel

#schema
class User(BaseModel):
    id: int
    name: str
    is_active: bool


input_data = {
    "id": 10,
    "name": "Harsh",
    "is_active": True 
}

user = User(**input_data)

print(user)















# -------------------------------------------------------------------------
#assignment
#--------------------------------------------------------------------------
from pydantic import BaseModel

# TODO: Create Product model with id, name, price, in stock


Class Product(BaseModel):
    product_id : int
    product_name:str
    product_price:int
    in_stock:bool
    
data = {"product_id" : 1 , "product_name" : "Adnex Hand Gripper","product_price" : 99 , in_stock:True}


product = Product(**data)

print(product)
