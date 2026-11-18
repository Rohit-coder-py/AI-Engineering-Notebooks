
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

while True:
    user_input = input("You: ")

    response = llm.invoke(user_input)

    print("AI:", response.content)
