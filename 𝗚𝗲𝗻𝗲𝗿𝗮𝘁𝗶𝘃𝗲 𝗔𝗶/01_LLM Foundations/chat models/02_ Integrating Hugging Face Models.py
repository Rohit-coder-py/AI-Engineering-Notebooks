#this is all about hugging face

#we will use open source models directly from hugging face


#will learn how to use models from hugging face locally and also via api

# ====================================================
 1. Use via hugging face api (paid) 
===============================================
#lets load env

import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

print(hf_token)
# =======================================================

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4.1-Flash",
    huggingfacehub_api_token=hf_token,
    temperature=0.7,
)
model = ChatHuggingFace(llm=llm)

res = model.invoke("WARNING! max_new_token is not default parameter.max_new_token was transferred to model_kwargs.Please make sure that max_new_token is what you intended., What is this warning when i am trying to load my model from hugging face ")

print(res.content)