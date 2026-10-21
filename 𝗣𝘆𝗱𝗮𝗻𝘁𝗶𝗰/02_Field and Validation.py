# ========================================== Typing Module

from pydantic import BaseModel

from typing import Optional,List,Dict


name: str = "Harsh"
age: int = 18
skills: list[str] = ["Python", "Pydantic"]

print(skills)


class Cart(BaseModel):
    user_id: int
    items: List[str]
    quantities: Dict[str, int]


class BlogPost(BaseModel):
    title: str
    content: str
    image: str
    
    
# ========================================== Fields in Pydantic

from pydantic import BaseModel,Field
from typing import Optional,List,Dict


# TODO: Create Product model

# Fields:
# - product_id: int
# - name: str (minimum 3 characters)
# - price: float (must be > 0)
# - in_stock: bool (default True)

# TODO: Create one valid product
# TODO: Print the product
# TODO: Print the product as a dictionary using model_dump()


class Product(BaseModel):
    product_id : int
    name : str = Field(...,                              #(... means mandatory field)
                       min_length=3,
                       max_length = 50,
                       description = "Product Name",
                       examples= ["Air Fryer"])
    
    price : float = Field(...,
                          gt=0)
    
    category : Optional[str] =None
    in_stock: bool = True
    
    
sample_product = Product(
    product_id = 1,
    name = "Apple Peeler",
    price = 5,
    category = "Home",
    in_stock = True )

print(sample_product.model_dump())


