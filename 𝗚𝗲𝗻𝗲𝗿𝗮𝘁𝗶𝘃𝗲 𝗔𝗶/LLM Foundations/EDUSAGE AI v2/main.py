import os
from typing import Optional, List

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key
)


# 1. Define the Pydantic model
class Course(BaseModel):
    course_name: str
    instructor: Optional[str] = None
    duration_weeks: Optional[int] = None
    difficulty: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    prerequisites: Optional[str] = None
    video_lessons: Optional[int] = None
    practical_projects: Optional[int] = None
    student_rating: Optional[float] = None
    summary: str


# 2. Initialize the Pydantic output parser
parser = PydanticOutputParser(pydantic_object=Course)


# 3. Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI assistant that extracts structured information
from online course descriptions.

Extract the course information according to the provided schema.
Do not invent missing information.
Keep the summary concise.

{format_instructions}
"""),
    ("human", "{course_description}")
])


# ---------------- UI ----------------
st.set_page_config(page_title="Course Extractor", page_icon="📚")

st.title("Course Extractor")
st.write("Paste a course description to get its details as structured JSON.")

# 4. Get course description
course = st.text_area("Course description", height=250)

if st.button("Extract"):
    if not course.strip():
        st.warning("Enter a course description first.")
    else:
        with st.spinner("Extracting..."):
            try:
                # 5. Format the prompt with parser instructions
                final_prompt = prompt.invoke({
                    "course_description": course,
                    "format_instructions": parser.get_format_instructions()
                })

                # 6. Invoke the model
                response = model.invoke(final_prompt)

                # 7. Parse and validate the model output
                data = parser.parse(response.content)

                # 8. Display the result as JSON
                st.code(data.model_dump_json(indent=4), language="json")
            except Exception as e:
                st.error(f"Something went wrong: {e}")