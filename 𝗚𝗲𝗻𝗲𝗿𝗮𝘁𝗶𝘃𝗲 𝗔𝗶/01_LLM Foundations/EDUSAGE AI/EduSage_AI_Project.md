
# EduSage AI --- Smart Course Information Extractor

## 1. Problem Statement

**EduSage AI** is an AI-powered tool that helps online learning
platforms organize and analyze course information.

Every day, the platform receives unstructured text from different
sources, such as:

-   Course descriptions
-   Instructor biographies
-   Student feedback
-   Course announcements
-   Blog articles about learning
-   Course prerequisites and requirements

The information arrives as long, messy paragraphs, making it difficult
to organize and search manually.

------------------------------------------------------------------------

## 2. Your Task

Build an AI tool that takes a raw paragraph about an online course and
automatically extracts useful information.

### Sample Input

> Python for Data Science is a beginner-friendly online course created
> by instructor Ankit Sharma. The course was launched in 2025 and takes
> approximately 8 weeks to complete. Students learn Python fundamentals,
> NumPy, Pandas, data visualization, and basic machine learning. No
> prior programming experience is required. The course includes 40 video
> lessons, 5 practical projects, and weekly assignments. It has received
> an average student rating of 4.7 out of 5.

------------------------------------------------------------------------

## 3. What Your AI Tool Must Do

### 1. Accept Raw Text

The user provides a paragraph about a course.

### 2. Extract Structured Information

Identify the course name, instructor, duration, skills, prerequisites,
projects, and rating.

### 3. Generate a Summary

Produce a clean, concise description of the course.

### 4. Return Valid JSON

The output must follow a consistent structure that another application
can use.

### 5. Store the Result

Save the extracted course information in a database such as SQLite.

------------------------------------------------------------------------

## 4. Expected Output Structure

Your program should generate JSON resembling this:

``` json
{
  "course_name": "Python for Data Science",
  "instructor": "Ankit Sharma",
  "duration_weeks": 8,
  "difficulty": "Beginner",
  "skills": [
    "Python",
    "NumPy",
    "Pandas",
    "Data Visualization",
    "Machine Learning"
  ],
  "prerequisites": "No prior programming experience",
  "video_lessons": 40,
  "practical_projects": 5,
  "student_rating": 4.7,
  "summary": "A beginner-friendly course covering Python and essential data science tools."
}
```

> **Important:** This is an illustrative expected output, not code to
> copy. Your AI should extract the values from the input rather than
> hardcoding them.

------------------------------------------------------------------------

## 5. Technologies to Practice

  Component                Technology
  ------------------------ ---------------------------------
  LLM                      Groq API with a supported model
  Prompting and messages   LangChain
  Structured output        JSON / Pydantic
  Data processing          Python
  Database                 SQLite
  Optional interface       Streamlit

------------------------------------------------------------------------

## 6. Challenge Rules

-   Do not watch a solution for this project.
-   Do not hardcode the expected output.
-   Test your program with at least **three different course
    descriptions**.
-   Handle missing fields without inventing information.
-   Ensure the generated JSON is valid.
-   Save the final structured records in your database.

------------------------------------------------------------------------

## 7. Suggested Development Stages

1.  Connect to the LLM and get a response.
2.  Write a prompt that asks the model to extract the required fields.
3.  Convert the response into structured data.
4.  Validate the structure and data types.
5.  Handle missing or uncertain information.
6.  Store the result in SQLite.
7.  Test with multiple course descriptions.

------------------------------------------------------------------------

## Project Goal

The goal is not just to make an AI API call. It is to understand how
**unstructured text becomes structured data** through an LLM-powered
pipeline.
