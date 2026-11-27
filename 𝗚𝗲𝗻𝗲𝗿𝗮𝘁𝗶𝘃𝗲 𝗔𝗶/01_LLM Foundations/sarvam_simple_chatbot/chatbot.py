import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
if not api_key or api_key == "PASTE_NEW_KEY_HERE":
    raise SystemExit("Add your new Sarvam API key to the .env file first.")

client = SarvamAI(api_subscription_key=api_key)

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not user_input:
        continue

    try:
        response = client.chat.completions(
            model="sarvam-105b-conversations",
            messages=[{"role": "user", "content": user_input}]
        )
        print("Bot:", response.choices[0].message.content)
    except Exception as error:
        print("API error:", error)
