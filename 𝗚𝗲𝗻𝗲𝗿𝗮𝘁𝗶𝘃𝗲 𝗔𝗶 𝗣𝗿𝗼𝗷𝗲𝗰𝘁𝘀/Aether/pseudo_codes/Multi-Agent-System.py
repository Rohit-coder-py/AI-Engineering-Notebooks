import os

import json
from dotenv import load_dotenv
import requests
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from rich import print
from tavily import TavilyClient
from pypdf import PdfReader


load_dotenv()

st.write("Multi Agent System")

# 1. RESEARCHER TOOL

search_tool = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def researcher_agent(topic: str) -> str:
    """Performs detailed research on the provided topic using Tavily Search."""

    response = search_tool.search(
        query=f"Perform detailed research on {topic}",
        search_depth="advanced",
        max_results=4
    )

    results = response.get("results", [])

    if not results:
        return f"No research results found for {topic}."

    research_results = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "No URL available")
        snippet = r.get("content", "No content available")

        research_results.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {snippet[:500]}..."
        )

    return (
        f"Research Results on: {topic}\n\n"
        + "\n\n".join(research_results)
    )



#2. Document Analyst Agent


@tool
def document_analyst_agent(question: str) -> str:
    """Answers user questions using the uploaded PDF document."""

    # 1. Read the PDF
    reader = PdfReader(file_upload)

    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            documents.append(Document(
                page_content=text,
                metadata={"page": page_number + 1}
            ))

    # 2. Chunking the PDF
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=12
    )

    total_chunks = splitter.split_documents(documents)

    # 3. Create embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # 4. Create vector database
    vector_db = FAISS.from_documents(
        documents=total_chunks,
        embedding=embedding_model
    )

    # 5. Retrieve relevant documents
    retreived_docs = vector_db.similarity_search(question, k=4)

    context = "\n\n".join(
        [doc.page_content for doc in retreived_docs]
    )

    # 6. LLM part
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt + "\n\nContext:\n{context}"),
            ("human", "{question}")])

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content




#3. Planner Agent

#creating it using create_agent()


@tool
planner_agent = create_agent(
    model=llm,
    tools=[document_analyst_agent, researcher_agent],
    system_prompt="""
    You are a Planner Agent.

    Your job is to analyze the user's request and decide
    which tools need to be executed.

    Available tools:
    1. document_analyst_agent: Answers questions using the uploaded PDF.
    2. researcher_agent: Performs web research on a topic.

    Rules:
    - Understand the user's request first.
    - Use document_analyst_agent for questions related to the uploaded PDF.
    - Use researcher_agent for external research.
    - Use both tools if the user requires information from
      the PDF and external research.
    - Do not call unnecessary tools.
    - If no tool is required, answer accordingly.
    - After executing the required tools, collect their results.
    - Pass the collected information in your final response.
    """)


#wRITER AGENT

writer_prompt = ChatPromptTemplate.from_messages(
    [(
            "system",
            """
            You are a Professional Writer Agent.

            Your job is to convert the information provided
            by the Planner Agent into a well-structured response.

            Rules:
            - Organize information properly.
            - Use meaningful headings and subheadings.
            - Use bullet points wherever required.
            - Use tables when they improve readability.
            - Maintain clarity and professionalism.
            - Do not add information that is not provided
              by the Planner Agent.
            - Preserve important facts and details.
            """
        ),
        (
            "human",
            """
            User Question:
            {question}

            Information from Planner Agent:
            {planner_output}

            Generate the final response.
            """)])

writer_agent = writer_prompt | llm



