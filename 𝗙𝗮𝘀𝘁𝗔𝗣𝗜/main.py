from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}


@app.get("/about")
def about():
    return {
        "name": "My First API",
        "language": "Python",
        "framework": "FastAPI"
    }



