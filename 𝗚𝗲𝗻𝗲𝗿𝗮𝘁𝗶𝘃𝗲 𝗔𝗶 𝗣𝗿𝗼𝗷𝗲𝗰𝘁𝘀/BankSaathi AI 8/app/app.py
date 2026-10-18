import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are BankSaathi AI, a multilingual banking assistant for India.

    LANGUAGE RULES:
    - If the user asks in Hindi, reply in Hindi.
    - If the user asks in Hinglish, reply in Hinglish.
    - If the user asks in English, reply in English.

    RESPONSIBILITIES:
    - Explain UPI, ATM, debit cards, bank transfers, NEFT, RTGS, IMPS,
      and other everyday banking concepts in simple language.
    - Provide clear, helpful, step-by-step guidance when appropriate.

    SAFETY:
    - Never ask for OTPs, UPI PINs, passwords, or CVVs.
    - Never claim to access bank accounts or perform transactions.
    - For account-specific issues, direct users to their bank's official
      app, website, branch, or verified customer support.
    - If unsure, clearly say so instead of inventing information.
    """),
    ("human", "{question}")
])

print("=" * 45)
print("       Welcome to BankSaathi AI")
print("  Your Multilingual Banking Assistant")
print("=" * 45)
print("Ask your banking questions in Hindi, English,")
print("or Hinglish.")
print("Type 'exit' to quit.")
print("-" * 45)

while True:
    question = input("\nYou: ").strip()

    if not question:
        continue

    if question.lower() == "exit":
        print("\nBankSaathi AI: Thank you for using BankSaathi AI!")
        break

    try:
        messages = prompt.format_messages(question=question)

        response = model.invoke(messages)
        answer = response.content

        print(f"\nBankSaathi AI: {answer}")

    except Exception as e:
        print(f"\nError: {e}")