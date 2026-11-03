import os

from dotenv import load_dotenv



from langchain_tavily import TavilySearch


load_dotenv()


search = TavilySearch(
    max_results = 5)

res = search.invoke({"query" : "Provide me latest  breaking news "})


from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your job is to summarize the provided news headlines and provide it to your . In the end , provide 5 key points from overall headlines"),
        ("human", "{news_headlines}"),
    ]
)

prompt = template.invoke({
    "news_headlines": res['results']})

res = llm.invoke(prompt)

print(res.content)


