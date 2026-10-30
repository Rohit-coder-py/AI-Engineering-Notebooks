#learning how to upload files in fastapi

from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    return "Hello"