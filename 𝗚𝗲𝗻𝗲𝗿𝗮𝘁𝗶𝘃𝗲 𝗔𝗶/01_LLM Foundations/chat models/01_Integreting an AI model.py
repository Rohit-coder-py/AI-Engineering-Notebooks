#part 1: Integreting an ai model 

import os
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv("GOOGLE_API_KEY")
grok_api = os.getenv("GROQ_API_KEY")


#both key loaded successfully


import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# # Initialize Google Gemini chat model
# model = init_chat_model("google_genai:gemini-3.8-flash")
# 
# 
# print(model.model)

# Send a test message
# response = model.invoke("Who is Heyy_letscodee on instagram")

# print(response.content[0]['text'])


#methord 2 : using the model class methord 9specific model class and not flexible)

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")

res = model.invoke("Full form of API")

final_res = res.content[0]["text"].replace("*", "")

print(final_res)



#Part 1 completed
# ===================================================================




# PART 2 : INTEGRATING HUGGING FACE MODELS

