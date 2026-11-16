# Al Study Material Generator

# Input: Any topic.
# . Node 1: Research topic
# . Node 2: Explain concepts
# . Node 3: Generate examples
# . Node 4: Create MCQs

""" An Agentic AI application that automatically generates comprehensive study materials on any given topic."""

#========================================================

import os
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


#first of all lets create states

class StudyState(TypedDict):
    study_topic: str
    research_result: str
    explained_result: str
    example_result: str
    mcq_result: str
    
    
#llm

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7)

    

#multiple nodes creation


def researcher_node(state: StudyState) -> dict:

    """Step 1: Research the given topic."""

    researcher_prompt = f"""
    You are an expert researcher.

    Your task is to research the following topic and provide a comprehensive research report.

    Topic: {state["study_topic"]}

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

    """

    response = llm.invoke(example_prompt)

    return {
        "example_result": response.content
    }


#node 4 : to test knowlege we need some mcq from the provided topic


def mcq_node(state: StudyState) -> dict:

    mcq_prompt = f"""
    You are an expert examination paper setter.

    Generate exactly 5 multiple-choice questions.

    Topic: {state["study_topic"]}

    Key Concepts:
    {state["explained_result"][:4000]}

    Practical Examples:
    {state["example_result"][:1500]}

    Requirements:
    1. Four options per question (A, B, C, D).
    2. One correct answer.
    3. Short explanation (1-2 lines).
    4. Cover different concepts.
    5. Avoid repetitive questions.
    """

    response = llm.invoke(mcq_prompt)

    return {
        "mcq_result": response.content
    }






#now all nodes and graph is ready for AI study material

#Now next Practical Step is: Create  a graph using that state and multiple nodes using EDGES


from langgraph.graph import StateGraph , START , END


graph = StateGraph(StudyState)             #graph created now adding nodes



# Add nodes

graph.add_node("researcher", researcher_node)

graph.add_node("explainer", explainer_node)

graph.add_node("examples", example_node)
graph.add_node("mcqs", mcq_node)


    
#add edges (sequential - one after another)


graph.add_edge(START , "researcher")
graph.add_edge("researcher","explainer")
graph.add_edge("explainer","examples")
graph.add_edge("examples","mcqs")

graph.add_edge("mcqs",END)


# Compile
app = graph.compile()

#======================UI==================================

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx(suppress_warning=True) is not None:

    # page settings (must be the first streamlit command)
    st.set_page_config(page_title="AI Study Material Generator")


    # Step 2: CSS for the Origami Folded Corner look
    # every card is "paper" with its top-right corner cut and a folded flap on top

    ui_css = """
    <style>
    /* page background */
    .stApp { background: #efe6d2; }
    .block-container { max-width: 900px; }

    /* paper card: top-right corner is cut diagonally (40px) */
    div[class*="st-key-fold"] {
        position: relative;
        background: #fffdf7;
        padding: 22px 28px;
        margin-bottom: 18px;
        clip-path: polygon(0 0, calc(100% - 40px) 0, 100% 40px, 100% 100%, 0 100%);
    }

    /* the folded flap: a small shaded triangle on the cut corner */
    div[class*="st-key-fold"]::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 40px;
        height: 40px;
        background: linear-gradient(45deg, #c4ad80 0%, #eadfc5 50%, transparent 50%);
    }

    /* text colours inside the cards */
    div[class*="st-key-fold"] p,
    div[class*="st-key-fold"] li,
    div[class*="st-key-fold"] label { color: #3d3326; }
    div[class*="st-key-fold"] h1,
    div[class*="st-key-fold"] h2,
    div[class*="st-key-fold"] h3 { color: #b4472f; }

    /* input box */
    div[class*="st-key-fold"] input { background: #ffffff; color: #3d3326; }

    /* button with a small folded corner too */
    .stButton > button {
        background: #c8553d;
        color: #ffffff;
        border: none;
        border-radius: 0;
        clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 0 100%);
    }
    .stButton > button:hover { background: #a8432e; color: #ffffff; }
    </style>
    """

    st.markdown(ui_css, unsafe_allow_html=True)


    # Step 3: remember the result, so it stays on screen after the page reruns

    if "ui_result" not in st.session_state:
        st.session_state["ui_result"] = None


    # Step 4: header card

    with st.container(key="fold_header"):
        st.markdown("#  AI Study Material Generator")
        st.markdown("Enter any topic and get research, explanation, examples and MCQs.")


    # Step 5: input card (topic box + button)

    with st.container(key="fold_input"):
        ui_topic = st.text_input("Study Topic", placeholder="e.g. Neural Networks")
        ui_clicked = st.button("Generate Study Material")


    # Step 6: when the button is clicked, run your existing graph (app)

    if ui_clicked:
        if ui_topic.strip() == "":
            st.warning("Please enter a study topic first.")
        else:
            with st.spinner("Agents are working... this can take a minute"):
                st.session_state["ui_result"] = app.invoke({"study_topic": ui_topic})


    # Step 7: show one card for each node output

    ui_result = st.session_state["ui_result"]

    if ui_result is not None:

        with st.container(key="fold_research"):
            st.markdown("## 🔍 Research")
            st.markdown(ui_result["research_result"])

        with st.container(key="fold_explained"):
            st.markdown("## 🧠 Explanation")
            st.markdown(ui_result["explained_result"])

        with st.container(key="fold_examples"):
            st.markdown("## 💻 Examples")
            st.markdown(ui_result["example_result"])

        with st.container(key="fold_mcqs"):
            st.markdown("## ✅ MCQs")
            st.markdown(ui_result["mcq_result"])


    # Step 8: stop here, so the terminal input() below does not run inside Streamlit

    st.stop()

#========================================================
# END OF UI SECTION
#========================================================


learning_topic = input("Enter your study topic:")

result = app.invoke({"study_topic": learning_topic})

print(result["research_result"])
print(result["explained_result"])
print(result["example_result"])
print(result["mcq_result"])