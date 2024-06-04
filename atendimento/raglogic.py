from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS 
from langchain.embeddings import OpenAIEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

vector_store = FAISS.load_local('atendimento/faiss_index', embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_k = 2)

def junta_docs(docs):
    return '\n\n'.join([doc.page_content for doc in docs])

def get_prompt(query):

    return f"""Responda a query utilizando o contexto disponibilizado:
    Query: {query}

    Contexto:{junta_docs(retriever.invoke(query))}"""

