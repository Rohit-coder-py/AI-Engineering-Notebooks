# 
# import os
# import requests
# from dotenv import load_dotenv
# 
# # Load environment variables
# load_dotenv()
# 
# API_KEY = os.getenv("OPENROUTER_API_KEY")
# 
# url = "https://openrouter.ai/api/v1/chat/completions"
# 
# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }
# 
# data = {
#     "model": "openrouter/free",
#     "messages": [
#         {
#             "role": "user",
#             "content": "Explain Agentic AI in simple words."
#         }
#     ]
# }
# 
# response = requests.post(url, headers=headers, json=data)
# 
# response.raise_for_status()
# 
# result = response.json()
# 
# print(result["choices"][0]["message"]["content"])




import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {"role": "user", "content": "Explain Agentic AI"}
    ]
)

print(response.choices[0].message.content)

