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
TXT_PATH = os.path.join(APP_PATH,"..","krishimitra_ai_notes","farming_knowledge_notes.txt") 

#document loaders

from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate



template = ChatPromptTemplate.from_messages([
    ("system", "You are KrishiMitra AI, a helpful farming assistant. Answer using the provided document.and also if the provided pdf/dataset is not related to farming you can simple return a warning that this document isnt related to farming so answering from internet or any source you are answering but always warn and suggest to change the uploaded document to get better answers  "),
    ("human", "Document:\n{content}\n\nQuestion: {question}")
])


data = TextLoader(TXT_PATH,encoding = "utf-8")

document = data.load()

content = document[0].page_content

question = input("Ask your farming question: ")


prompt = template.invoke({
    "content": content,
    "question": question
})

result = model.invoke(prompt)

print(result.content)