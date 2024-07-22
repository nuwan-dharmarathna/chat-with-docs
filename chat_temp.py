import streamlit as st
from streamlit_chat import message

def main():
    st.set_page_config(
        page_title="Chat with your Data",
        page_icon="🤖"
    )
    
    st.header("Chat with your own Data 🤖")
    
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")
    
    message("Hello how can I assist you!")
    message("Hi, can you read a book", is_user=True)


if __name__ == "__main__":
    main()