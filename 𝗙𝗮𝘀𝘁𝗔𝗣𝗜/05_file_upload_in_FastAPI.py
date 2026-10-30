#learning how to upload files in fastapi

from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI, File, UploadFile


app = FastAPI()

#Important: python-multipart is required by FastAPI to process uploaded form data.


@app.get("/")
def home():
    return "Hello"


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


#python built in module : io


import io

data = r"C:\Users\rohit\Downloads\fake_job_postings_20_rows.csv"

file = io.StringIO(data)

print(file.read())

# 
# #Approach : StreamingResponse
# - Read a small chunk of the file.
# - Send that chunk to the client.
# - Read the next chunk.
# - Continue until the file is completely sent.

from fastapi.responses import StreamingResponse









# ===================================

# async is a Python keyword used to define an asynchronous function.

async def welcome():
    return "Hello"


p = welcome()

print(p)

# -------------------------------------------
import asyncio

async def welcome():
    await asyncio.sleep(2)
    return "Hello Rohit"

async def main():
    result = await welcome()
    print(result)

asyncio.run(main())