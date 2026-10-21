#load data from any website

from langchain_community.document_loaders import WebBaseLoader


url = "https://ask-your-pdf-genai.streamlit.app/"

data = WebBaseLoader(url)


docs = data.load()

print(docs[0].page_content)