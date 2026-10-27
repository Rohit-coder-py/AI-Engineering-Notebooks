from typing import List, Optional
from pydantic import BaseModel  # type: ignore

class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int
    name: str
    address: Address
    
class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comment']] = None


Comment.model_rebuild()    #import function name : Forward Refrence A reference to a type that is defined later or not yet fully resolved.


address = Address(
    street="123 something",
    city="Jaipur",
    postal_code="10001"
)


user = User(
    id=1,
    name="Hitesh",
    address=address,
)

comment = Comment(
    id=1,
    content="First Comment",
    replies=[
        Comment(id=2, content="reply1"),
        Comment(id=2, content="reply2")])



#========================================================
#                      PRACTICE
#========================================================

from pydantic import BaseModel  
from typing import List

# TODO: Create Course model
# Each Course has modules
# Each Module has lessons

class Lessons(BaseModel):
    lesson_id :int
    topic : str
    
class Module(BaseModel):
    module_id : int = Field(...,ge=1)
    module_name = str
    module_lessons: List[Lessons]

class Course(BaseModel):
    course_id = int =Field(...,ge = 1)
    course_title = str
    course_modules = List[Module]
    