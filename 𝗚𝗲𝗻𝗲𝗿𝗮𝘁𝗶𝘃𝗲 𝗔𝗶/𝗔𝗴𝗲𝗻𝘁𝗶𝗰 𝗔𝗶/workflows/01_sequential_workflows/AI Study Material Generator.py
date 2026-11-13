# Al Study Material Generator

# Input: Any topic.
# . Node 1: Research topic
# . Node 2: Explain concepts
# . Node 3: Generate examples
# . Node 4: Create MCQs

""" An Agentic AI application that automatically generates comprehensive study materials on any given topic."""



import os
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI


#first of all lets create states

class StudyState(TypedDict):
    study_topic: str
    research_result: str
    explained_result: str
    example_result: str
    mcq_result: str
    
    

#node creation
    
    
#connect to OmniRoute
llm = ChatOpenAI(
    model="ddgw/tinfoil/gpt-oss-120b",
    api_key=os.getenv("OMNIROUTE_API_KEY"),
    base_url=os.getenv("OMNIROUTE_BASE_URL"),
    temperature=0.7
)

    

#multiple nodes


def researcher_node(state: StudyState) -> dict:

    """Step 1: Research the given topic."""

    researcher_prompt = f"""
    You are an expert researcher.

    Your task is to research the following topic and provide a comprehensive research report.

    Topic: {state["study_topic"]}

    Include:
    1. Introduction
    2. Background
    3. Important concepts
    4. Key terminology
    5. Applications
    6. Advantages and limitations
    """

    response = llm.invoke(researcher_prompt)

    return {"research_result": response.content}


#node 2 : after reseach we have to provide explain concept of researcher node
    
    
def explainer_node(state: StudyState)  ->  dict:

    explainer_prompt = f"""
    You are an expert teacher.

    Explain the following research material
    in a beginner-friendly and detailed manner.

    Research Material:{state["research_result"]}

    Include:
    1. Detailed explanations
    2. Important definitions
    3. Step-by-step explanations
    4. Technical terminology
    """

    response = llm.invoke(explainer_prompt)

    return {
        "explained_result": response.content
    }
    
    

    
#node 3 : after explanation and research we need some examples to explain berifely


def example_node(state: StudyState) -> dict:

    example_prompt = f"""
    You are an expert practical instructor.

    Generate practical examples for the following topic.

    Topic: {state["study_topic"]}

    Concepts:{state["explained_result"]}

    Include:
    1. Real-world examples
    2. Python code examples where applicable
    3. Practical use cases
    4. Explanation of each example
    """

    response = llm.invoke(example_prompt)

    return {
        "example_result": response.content
    }


#node 4 : to test knowlege we need some mcq from the provided topic

def mcq_node(state: StudyState) -> dict:

    mcq_prompt = f"""
    You are an expert examination paper setter.

    Generate 5 multiple-choice questions.

    Topic: {state["study_topic"]}

    Study Material:{state["explained_result"]}

    Include:
    1. Four options per question
    2. Correct answer
    3. Short explanation (1-2 lines) 
    """

    response = llm.invoke(mcq_prompt)

    return {
        "mcq_result": response.content
    }