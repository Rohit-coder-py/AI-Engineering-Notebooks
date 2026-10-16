import os
import json

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Course Info Extractor", page_icon="🎓", layout="centered")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI assistant that extracts structured information
from online course descriptions.

Analyze the following course description and extract:

- course_name
- instructor
- duration_weeks
- difficulty
- skills
- prerequisites
- video_lessons
- practical_projects
- student_rating
- summary

Rules:
1. Return only valid JSON. Do not use Markdown code blocks.
2. Do not invent missing information. Use null for missing values.
3. Store skills as a list of strings.
4. Use numbers for duration, video lessons, projects, and rating.
5. Keep the summary concise.
"""),
    ("human", "{course_description}")
])


def show(value):
    return "—" if value is None else value


# ---------- UI ----------
st.title("🎓 Course Info Extractor")
st.caption("Paste an online course description and get structured information from it.")

course = st.text_area(
    "Course description",
    height=250,
    placeholder="Paste the course description here...",
)

extract = st.button("Extract", type="primary", use_container_width=True)

if extract:
    if not course.strip():
        st.warning("Please enter a course description.")
    else:
        try:
            with st.spinner("Extracting..."):
                final_prompt = prompt.invoke({"course_description": course})
                response = model.invoke(final_prompt)
                data = json.loads(response.content)
        except json.JSONDecodeError:
            st.error("The model did not return valid JSON. Please try again.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
        else:
            st.divider()
            st.header(show(data.get("course_name")))
            st.write(f"**Instructor:** {show(data.get('instructor'))}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Duration (weeks)", show(data.get("duration_weeks")))
            c2.metric("Difficulty", show(data.get("difficulty")))
            c3.metric("Student rating", show(data.get("student_rating")))

            c4, c5 = st.columns(2)
            c4.metric("Video lessons", show(data.get("video_lessons")))
            c5.metric("Practical projects", show(data.get("practical_projects")))

            st.subheader("Skills")
            skills = data.get("skills")
            if skills:
                st.write(" ".join(f"`{s}`" for s in skills))
            else:
                st.write("—")

            st.subheader("Prerequisites")
            prereq = data.get("prerequisites")
            if isinstance(prereq, list):
                if prereq:
                    for p in prereq:
                        st.write(f"- {p}")
                else:
                    st.write("—")
            else:
                st.write(show(prereq))

            st.subheader("Summary")
            st.write(show(data.get("summary")))

            with st.expander("Raw JSON"):
                st.code(json.dumps(data, indent=4, ensure_ascii=False), language="json")