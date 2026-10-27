"""
Pydantic Parsers — Practical Learning File
==========================================

Install:
    pip install pydantic

Pydantic parsers help convert incoming data into Python values/models while
checking that the data matches the expected types and constraints.

In Pydantic v2, the main methods are:
    1. Model.model_validate()       -> validate Python objects, commonly dicts
    2. Model.model_validate_json() -> parse and validate JSON strings/bytes
    3. model.model_dump()           -> serialize model to a Python dict
    4. model.model_dump_json()      -> serialize model to a JSON string
    5. TypeAdapter                 -> validate types without defining a BaseModel

Note:
    These are Pydantic v2 APIs. Older tutorials may use parse_obj() or
    parse_raw(); prefer the v2 methods for new code.
"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, TypeAdapter, ValidationError


# ------------------------------------------------------------
# 1. Define a model
# ------------------------------------------------------------

class Address(BaseModel):
    city: str
    postal_code: str


class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    email: str
    created_at: datetime
    address: Address


sample_dict = {
    "name": "Aarav",
    "age": "21",  # Pydantic can coerce this string to an integer
    "email": "aarav@example.com",
    "created_at": "2026-10-27T09:00:00",
    "address": {
        "city": "Lucknow",
        "postal_code": "226001",
    },
}


# ------------------------------------------------------------
# 2. model_validate(): validate a Python object / dictionary
# ------------------------------------------------------------

print("\n1) model_validate()")
user = User.model_validate(sample_dict)
print(user)
print("Age type:", type(user.age).__name__)
print("Nested city:", user.address.city)


# ------------------------------------------------------------
# 3. model_validate_json(): parse and validate JSON text
# ------------------------------------------------------------

print("\n2) model_validate_json()")
json_text = """
{
    "name": "Meera",
    "age": 22,
    "email": "meera@example.com",
    "created_at": "2026-10-27T09:15:00",
    "address": {
        "city": "Kanpur",
        "postal_code": "208001"
    }
}
"""

user_from_json = User.model_validate_json(json_text)
print(user_from_json)
print("City:", user_from_json.address.city)


# ------------------------------------------------------------
# 4. model_dump(): serialize model to a Python dictionary
# ------------------------------------------------------------

print("\n3) model_dump()")
user_dict = user.model_dump()
print(user_dict)
print("Result type:", type(user_dict).__name__)


# ------------------------------------------------------------
# 5. model_dump_json(): serialize model to a JSON string
# ------------------------------------------------------------

print("\n4) model_dump_json()")
user_json = user.model_dump_json(indent=2)
print(user_json)
print("Result type:", type(user_json).__name__)


# ------------------------------------------------------------
# 6. TypeAdapter: validate a type without a BaseModel
# ------------------------------------------------------------

print("\n5) TypeAdapter")
# Validate a list of integers. Values that can safely be converted may be
# coerced; invalid values raise ValidationError.
integer_list_adapter = TypeAdapter(list[int])
numbers = integer_list_adapter.validate_python([1, "2", 3])
print("Validated integers:", numbers)
print("Element types:", [type(number).__name__ for number in numbers])

# TypeAdapter can also parse JSON directly.
numbers_from_json = integer_list_adapter.validate_json('[4, "5", 6]')
print("Integers from JSON:", numbers_from_json)


# ------------------------------------------------------------
# 7. Annotated types and constraints with TypeAdapter
# ------------------------------------------------------------

print("\n6) TypeAdapter with a constraint")
PositiveInt = Annotated[int, Field(gt=0)]
positive_int_adapter = TypeAdapter(PositiveInt)

print("Valid positive integer:", positive_int_adapter.validate_python("7"))

try:
    positive_int_adapter.validate_python(-3)
except ValidationError as error:
    print("Invalid value caught:")
    print(error)


# ------------------------------------------------------------
# 8. Handling invalid data safely
# ------------------------------------------------------------

print("\n7) Handling invalid model data")
bad_data = {
    "name": "Sam",
    "age": -5,  # Invalid: age must be between 0 and 120
    "email": "sam@example.com",
    "created_at": "not-a-date",
    "address": {
        "city": "Delhi",
        "postal_code": "110001",
    },
}

try:
    User.model_validate(bad_data)
except ValidationError as error:
    print("Pydantic found validation errors:")
    print(error)


# ------------------------------------------------------------
# Quick recap
# ------------------------------------------------------------
#
# model_validate(data)
#     Python dict/object -> validated Pydantic model
#
# model_validate_json(json_text)
#     JSON text/bytes -> validated Pydantic model
#
# model_dump()
#     Pydantic model -> Python dict
#
# model_dump_json()
#     Pydantic model -> JSON string
#
# TypeAdapter(SomeType)
#     Validate/parse a type such as list[int] without making a BaseModel
#
# Important:
# Parsing/validation is not the same as guaranteeing every input is correct.
# Invalid values raise pydantic.ValidationError; catch it when appropriate.
