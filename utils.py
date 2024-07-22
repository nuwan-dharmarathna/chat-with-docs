from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

# define llm
def get_llm():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    return llm