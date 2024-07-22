import streamlit as st

from chat_with_pdf import pdf_chat
from chat_with_website import website_chat
from chat_with_csv import csv_chat

def init():
    st.set_page_config(
        page_title="ChatVault",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Chat with your Data 🤖")
       
def side_bar_option():
    #sidebar
    with st.sidebar:
        option = st.selectbox(
            "Select your Option", 
            ["Chat with PDF 📃", "Chat with Website 🌐", "Chat with CSV 📈", "Chat with mySQL DB 🐬"],
            )
    
    if option == "Chat with PDF 📃":
        
        with st.sidebar:
            file = st.file_uploader("Upload your PDF file", type="pdf")
            
        if file is None:
            st.info("Please upload your PDF file")
        else:
            pdf_chat(file)
            
    elif option == "Chat with Website 🌐":
        with st.sidebar:
            website_url = st.text_input("Website URL")
        
        if website_url is None or website_url == "":
            st.info("Please enter your website URL")
        else:
            website_chat(website_url)
        
    elif option == "Chat with CSV 📈":
        with st.sidebar:
            file = st.file_uploader("Upload your CSV file", type="csv")
        if file is None:
            st.info("Please upload your CSV file")
        else:
            csv_chat(file)
    
    elif option == "Chat with mySQL DB 🐬":
        with st.sidebar:
            db_name = st.text_input("Database Name")
            db_user = st.text_input("Database User")
            db_password = st.text_input("Database Password", type="password")
            db_host = st.text_input("Database Host")
            db_port = st.text_input("Database Port")
            st.button("Connect")

def main():
    
    init()
    
    side_bar_option()
    
    
if __name__ == "__main__":
    main()