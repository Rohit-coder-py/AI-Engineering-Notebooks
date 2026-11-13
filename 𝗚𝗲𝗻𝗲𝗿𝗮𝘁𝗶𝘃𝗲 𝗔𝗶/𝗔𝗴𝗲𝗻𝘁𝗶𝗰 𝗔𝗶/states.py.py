# so overall we have to create a Graph 
# the first thing we create in a LangGraph Graph is State


#so now we are creating a graph 
#and the first thing you create is a state 


import os 

#1) using typed DICT (Most common approach)

from typing import TypedDict

class State(TypedDict):
    topic : str
    summary : str 
    mcq : str 


#2) pydantic approach 
#it is good at data validation and type checking at  runtime 

from pydantic import BaseModel, field_validator

class State(BaseModel):
    topic : str 
    mcq :str 
    summary : str = ""

    @field_validator
    def score_positive(cls,v):
        if len(v) < 0:
            raise ValueError("too short")

#python dataclaseess 

#standard python dataclass but it is least used

from dataclasses import dataclass, field 

@dataclass
class State:
    topic : str = ""
    summary  : str = ""
    messages : list = field(default_factory=list)


from langgraph.graph import MessagesState

class State(MessagesState):
    # messages field is already included with add_messages reducer
    # just add your extra fields
    user_name: str
    language: str