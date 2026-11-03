# RunnablePassthrough is a Runnable that passes the input through unchanged without modifying it.

from langchain_core.runnables import RunnablePassthrough

runnable = RunnablePassthrough()

response = runnable.invoke("Hello LangChain!")

# print(response)]


import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

parser = StrOutputParser()

simple_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

technical_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} technically."
)

simple_chain = simple_prompt | llm | parser
technical_chain = technical_prompt | llm | parser

chain = RunnableParallel(
    original_topic=RunnablePassthrough(),
    simple_explanation=simple_chain,
    technical_explanation=technical_chain
)

response = chain.invoke({
    "topic": "Artificial Intelligence"
})

print(response)