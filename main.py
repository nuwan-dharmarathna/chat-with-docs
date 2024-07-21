import streamlit as st
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_openai import ChatOpenAI


import os
from dotenv import load_dotenv

load_dotenv()



def main():
    st.set_page_config(page_title="Ask your CSV 📈")
    st.header("Ask your CSV 📈")
    
    user_file = st.file_uploader("Upload your CSV File", type="csv")
    
    if user_file is not None:
        usr_question = st.text_input("Ask a question about your CSV")
        
        #implement language model
        llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            api_key= os.getenv('OPENAI_API_KEY')
        )
        
        #implement agent
        agent = create_csv_agent(
            llm,
            user_file,
            verbose=True,
            allow_dangerous_code=True
        )
        
        if usr_question is not None and usr_question != "":
            
            response = agent.run(usr_question)
            
            st.write(response)
    

if __name__ == "__main__":
    main()
    