from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import openai

# set env varialble
openai.api_key = os.environ['OPENAI_API_KEY']

import warnings

warnings.filterwarnings(
    "ignore", 
    category=DeprecationWarning, 
    message=".*LangChainDeprecationWarning.*"
)


# load PDF

loader = PyPDFLoader('./data/doc1.pdf')
doc = loader.load()

# Splitting

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
) 

splitter = text_splitter.split_documents(documents=doc)

print(f'length of splitter: {len(splitter)}')


# Embedding

embedding = OpenAIEmbeddings()

# Vectorstore

persist_directory = 'docs/chroma/'

vector_db = Chroma.from_documents(
    documents=splitter,
    embedding=embedding, 
    persist_directory=persist_directory,
)

print(f'vector_db collection count: {vector_db._collection.count()}')


# Initialize LLM

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
)

# build prompt

template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:

"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=['context', 'question'],
    template=template,
)

# Memory

memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True,
)

chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=vector_db.as_retriever(),
    memory=memory,
)

question = "Give me a summary of this content."
result = chain.invoke({"question": question})
print(result['answer'])
