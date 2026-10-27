
#model validator and field validator

from pydantic import (Field,BaseModel,field_validator,model_validator,computed_field)
from typing import Optional,List,Dict


class User(BaseModel):
    username: str
    
    @field_validator('username')#to vaidate a single field and add conditions or something on a field
    @classmethod
    def username_validator(cls,v):
        if len(v)<4:
            raise ValueError("Username alseat 4 characters")
        return  v
            
            
     
class SignUpData(BaseModel):
    password: str
    confirm_password : str
    
    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Please match both fields")
        return self
    

class Product(BaseModel):
    price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:           #return type annotation this is ->
        return self.price * self.quantity
    
       
#=================================================
#                  PRACTICE
#=================================================

# TODO: Create Booking model
# Fields:
# - user_id: int
# - room_id: int
# - nights: int (must be >= 1)
# - rate_per_night: float
# Also, add computed field: total_amount = nights * rate_per_night


class BookingModel(BaseModel):
    user_id : int
    room_id :int
    nights : int = Field(...,ge=1)
    rate_per_night:float
    
    @field_validator('nights')
    @classmethod
    def night_validator(cls, value):
        if value < 1:
            raise ValueError("Value of Night should be greater than or equal to 1")
        return value
        
        
    @computed_field
    @property
    
    def total_amount(self) -> float:
        return self.nights * self.rate_per_night
    
            
            
# =================================================
#                      TESTING
# =================================================

from pydantic import ValidationError


# ---------- TEST 1: Valid User ----------

print("\n--- TEST 1: Valid User ---")

user = User(username="rohit")
print(user)


# ---------- TEST 2: Invalid User ----------

print("\n--- TEST 2: Invalid User ----------")

try:
    user = User(username="raj")
    print(user)
except ValidationError as e:
    print(e)


# ---------- TEST 3: Matching Passwords ----------

print("\n--- TEST 3: Matching Passwords ---")

signup = SignUpData(
    password="abc123",
    confirm_password="abc123"
)
print(signup)


# ---------- TEST 4: Mismatching Passwords ----------

print("\n--- TEST 4: Mismatching Passwords ---")

try:
    signup = SignUpData(
        password="abc123",
        confirm_password="xyz789"
    )
    print(signup)
except ValidationError as e:
    print(e)


# ---------- TEST 5: Product Computed Field ----------

print("\n--- TEST 5: Product Computed Field ---")

product = Product(price=500, quantity=3)

print("Price:", product.price)
print("Quantity:", product.quantity)
print("Total Price:", product.total_price)
print("Product Dictionary:", product.model_dump())


# ---------- TEST 6: Valid Booking ----------

print("\n--- TEST 6: Valid Booking ---")

booking = BookingModel(
    user_id=101,
    room_id=201,
    nights=3,
    rate_per_night=1500
)

print(booking)
print("Total Amount:", booking.total_amount)
print("Booking Dictionary:", booking.model_dump())


# ---------- TEST 7: Invalid Booking ----------

print("\n--- TEST 7: Invalid Booking ---")

try:
    booking = BookingModel(
        user_id=101,
        room_id=201,
        nights=0,
        rate_per_night=1500
    )
    print(booking)
except ValidationError as e:
    print(e)
