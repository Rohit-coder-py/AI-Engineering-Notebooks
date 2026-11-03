import os

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

search = TavilySearch(
    max_results=5
)

res = search.invoke({
    "query": "Provide me latest breaking news"
})

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

template = ChatPromptTemplate([
    ("system", """
    You are a professional AI news summarizer.

    Your task:
    1. Summarize each news article separately.
    2. Provide a suitable heading for each article.
    3. Explain the news in simple language.
    4. Include the source URL.

    At the end, provide exactly 5 key takeaways
    covering the overall news.

    Do not make up facts or information.
    """),

    ("human", "{news_headlines}")
])

parser = StrOutputParser()

chain = template | llm | parser

response = chain.invoke({
    "news_headlines": res["results"]
})

print(response)