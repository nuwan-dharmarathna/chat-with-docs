import streamlit as st
from streamlit_chat import message as chat_msg

from utils import get_llm

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.messages import AIMessage, HumanMessage

def get_vector_store_from_url(url):
    # get the textin document form
    loader = WebBaseLoader(url)
    document = loader.load()
    
    #split the document into chunks
    splitter = RecursiveCharacterTextSplitter()
    document_chunks = splitter.split_documents(document)
    
    #create a vectorstore from chunks
    embedding = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(document_chunks, embedding)
    
    return vector_store

def get_context_retriever_chain(vector_store):
    # define llm
    llm = get_llm()
    
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevent to the conversation"),
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    # define llm
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    self_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retriever_chain, self_documents_chain)

def get_response(user_query):
    # create conversation chain
    
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    
    conversational_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversational_rag_chain.invoke({
        "chat_history":st.session_state.chat_history,
        "input":user_query
    })
    
    return response['answer']


def website_chat(website_url):
    
    #session state chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you")
        ]
        
    # vector store
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vector_store_from_url(website_url)
        
    #user query 
    user_query = st.chat_input("Type your message...")
    
    if user_query is not None and user_query != "":
        with st.spinner("Thinking..."):
            response = get_response(user_query)
            
        #append to the chat_history
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
        
    # conversations
    chat_history_ = st.session_state.get("chat_history", [])
    
    for i, msg in enumerate(chat_history_):
        if i % 2 != 0:
            chat_msg(msg.content, is_user=True, key=str(i)+'_user')
        else:
            chat_msg(msg.content, is_user=False, key=str(i)+'_ai')