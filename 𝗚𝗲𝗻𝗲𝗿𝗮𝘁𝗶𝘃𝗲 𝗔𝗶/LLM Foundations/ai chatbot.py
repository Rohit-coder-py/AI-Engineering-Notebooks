import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [SystemMessage(content=("You are a professional, friendly, and helpful AI assistant. "
            "Answer questions clearly, accurately, and respectfully. "
            "Use simple language and provide examples when helpful. "
            "Understand the user's context and remember relevant details "
            "from the conversation. "
            "Be polite, patient, and solution-oriented. "
            "If you don't know an answer, admit it instead of making "
            "up information. "
            "Keep answers concise unless more detail is requested. "
            "Never insult, mock, or criticize the user."))]

print("AI Chatbot Started! (Type 'exit' to stop)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(messages)

    messages.append(AIMessage(content = response.content))

    print("AI:", response.content)
    
print(messages)