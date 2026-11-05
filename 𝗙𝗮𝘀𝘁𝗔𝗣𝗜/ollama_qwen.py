from fastapi import FastAPI
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"


@app.get("/")
def home():
    return {"status": "Qwen API is running"}


@app.post("/chat")
def chat(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:0.6b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=300
    )

    return response.json()["message"]["content"]