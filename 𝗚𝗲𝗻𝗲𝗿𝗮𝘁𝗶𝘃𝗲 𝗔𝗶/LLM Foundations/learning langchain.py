# #installation 
# 
# import sys
# print(sys.executable)
# print(sys.version)
# 
# 
# 
# import langchain
# print(langchain.__version__)
# 
# 
# import langchain
# import langchain_core
# 
# print("LangChain verification successful!")
# print("-" * 40)
# 
# print("LangChain version:", langchain.__version__)
# print("LangChain location:", langchain.__file__)
# print("LangChain Core version:", langchain_core.__version__)
# print("LangChain Core location:", langchain_core.__file__)
# 
# print("-" * 40)
# print("Both packages imported successfully!")
#
# ----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("Google API key loaded successfully!")
else:
    print("API key not found!")
    
    