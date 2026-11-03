import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser


from langchain_core.runnables import RunnableParallel      #imp

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

#Create different prompts
simple_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words."
)

technical_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} using technical terminology."
)

example_prompt = ChatPromptTemplate.from_template(
    "Give one real-world example of {topic}."
)

#Create individual sequences
parser = StrOutputParser()

simple_chain = simple_prompt | llm | parser

technical_chain = technical_prompt | llm | parser

example_chain = example_prompt | llm | parser

# Create RunnableParallel
parallel_chain = RunnableParallel(
    simple=simple_chain,
    technical=technical_chain,
    example=example_chain
)

# now Execute all branches
response = parallel_chain.invoke({
    "topic": "Artificial Intelligence"
})

print(response)