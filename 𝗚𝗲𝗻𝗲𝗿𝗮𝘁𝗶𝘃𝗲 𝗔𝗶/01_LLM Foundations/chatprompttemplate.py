from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate([
    ("system", "You are a helpful AI assistant."),
    ("human", "Tell me about {topic}")
])

prompt = template.invoke({
    "topic": "Artificial Intelligence"
})

#system and human


#approach 2: using from template

from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_template(
    "Tell me about {topic} in simple language"
)

prompt = template.invoke({
    "topic": "Artificial Intelligence"
})

#approach 3 : using from messages


template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "Explain {topic}")
])