
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

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

course = input("Write course description :\n")

#inistilize the prompt
final_prompt = prompt.invoke({"course_description" : course})


import json

response = model.invoke(final_prompt)

data = json.loads(response.content)

print(json.dumps(data, indent=4, ensure_ascii=False))



