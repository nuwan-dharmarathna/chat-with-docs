import streamlit as st
from streamlit_chat import message as chat_msg

from utils import get_llm

from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.messages import AIMessage, HumanMessage

def get_response(file, user_query):
    # define llm
    llm = get_llm()
    
    # define agent
    agent = create_csv_agent(
        llm,
        file,
        allow_dangerous_code=True
    )
    
    # Define prompt template
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation"),
    ])
    
    # Get the current conversation history
    chat_history = st.session_state.get("chat_history", [])
    
    # Format the prompt
    formatted_prompt = prompt.format(
        chat_history=chat_history,
        input=user_query
    )
    
    return agent.run(formatted_prompt)

def csv_chat(file):
    # session state chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you")
        ]
    
    #user query
    user_query = st.chat_input("Type your message...")
    
    if user_query is not None and user_query != "":
        #response with spinnig
        with st.spinner("Thinking..."):
            response = get_response(file, user_query)
        
        #appent to chat_history
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
    
    #conversations
    chat_history_ = st.session_state.get("chat_history", [])
    
    for i, msg in enumerate(chat_history_):
        if i % 2 != 0:
            chat_msg(msg.content, is_user=True, key=str(i)+'_usr')
        else:
            chat_msg(msg.content, is_user=False, key=str(i)+'_ai')