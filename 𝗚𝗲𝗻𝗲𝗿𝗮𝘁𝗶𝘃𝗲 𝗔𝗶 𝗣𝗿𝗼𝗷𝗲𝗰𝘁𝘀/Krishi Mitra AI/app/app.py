from dotenv import load_dotenv

import os


load_dotenv()

api_key = os.getenv("GROK_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")


from langchain_groq import ChatGroq


model = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)


#basic settings

APP_PATH = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_PATH, "..", "assets", "logo.png")
TXT_PATH = os.path.join(APP_PATH,"..","krishimitra_ai_notes","notes.txt") 

#document loaders

from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate



prompt = ChatPromptTemplate.from_messages(
    [("system"), 
     ("human")]
    )




data = TextLoader(TXT_PATH,encoding = "utf-8")

document = data.load()

print(document[0].page_content)