import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Connect to OmniRoute
llm = ChatOpenAI(
    model="ddgw/tinfoil/gpt-oss-120b",
    api_key=os.getenv("OMNIROUTE_API_KEY"),
    base_url=os.getenv("OMNIROUTE_BASE_URL"),
    temperature=0.7
)

# Generate response
response = llm.invoke(
    "Explain what an AI agent is in simple words."
)

print(response.content)
