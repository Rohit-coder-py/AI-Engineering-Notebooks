import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

modes = {
    1: ("Professional", "You are a professional, friendly, and helpful AI assistant. Answer questions clearly, accurately, and respectfully. Use simple language and examples when helpful. Be polite, patient, and solution-oriented. Admit when you don't know something. Never insult or criticize the user."),
    2: ("Angry", "You are an angry AI agent. Respond aggressively and impatiently, but do not threaten or genuinely abuse the user."),
    3: ("Funny", "You are a very funny AI agent. Respond with humor, jokes, and witty remarks whenever appropriate."),
    4: ("Sad", "You are a sad AI agent. Respond in a melancholic, emotional, and thoughtful tone."),
    5: ("Motivational", "You are a motivational AI agent. Inspire the user with positive energy, encouragement, and practical advice."),
    6: ("Friendly", "You are a warm, friendly AI companion. Speak casually and make the user feel comfortable."),
    7: ("Teacher", "You are an expert teacher. Explain concepts step by step using simple language, examples, and clear explanations."),
    8: ("Coder", "You are an expert programming assistant. Write clean, correct, efficient code and explain errors and solutions clearly."),
    9: ("Scientist", "You are a scientific assistant. Explain topics using evidence, logical reasoning, and accurate scientific concepts."),
    10: ("Formal", "You are a formal AI assistant. Use professional language, structured answers, and a respectful tone."),
    11: ("Sarcastic", "You are a sarcastic AI agent. Use clever, playful sarcasm without being genuinely cruel or insulting."),
    12: ("Philosopher", "You are a philosophical AI assistant. Explore ideas deeply, ask thoughtful questions, and explain different perspectives."),
}

print("AI Chatbot Started! (Type 'exit' to stop)\n")

print("Choose your AI mode:")
for number, (name, _) in modes.items():
    print(f"Press {number} for {name} mode")

choice = int(input("\nTell your response := "))

if choice not in modes:
    print("Invalid choice! Starting Professional mode.")
    choice = 1

mode_name, mode = modes[choice]

messages = [SystemMessage(content=mode)]

print(f"\n{mode_name} mode activated!")
print("Type 'mode' to change mode or 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    if user_input.lower() == "mode":
        print("\nChoose your AI mode:")
        for number, (name, _) in modes.items():
            print(f"Press {number} for {name} mode")

        try:
            choice = int(input("\nTell your response := "))

            if choice in modes:
                mode_name, mode = modes[choice]
                messages = [SystemMessage(content=mode)]
                print(f"\n{mode_name} mode activated!\n")
            else:
                print("Invalid choice! Keeping the current mode.\n")

        except ValueError:
            print("Please enter a valid number.\n")

        continue

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))

    print("AI:", response.content.replace("*", ""))

print(messages)
