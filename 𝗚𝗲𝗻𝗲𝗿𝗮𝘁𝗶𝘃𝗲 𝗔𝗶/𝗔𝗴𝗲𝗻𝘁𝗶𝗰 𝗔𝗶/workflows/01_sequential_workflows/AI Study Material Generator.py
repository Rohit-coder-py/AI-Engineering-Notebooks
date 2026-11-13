# Al Study Material Generator

# Input: Any topic.
# . Node 1: Research topic
# . Node 2: Explain concepts
# . Node 3: Generate examples
# . Node 4: Create MCQs

""" An Agentic AI application that automatically generates comprehensive study materials on any given topic."""



import os
from typing import TypedDict

#first of all lets create states

class studystate(TypedDict):
    topic : str
    research_result = str
    explained_result = str
    example_result = str
    mcq_result = str
    
    

    
    