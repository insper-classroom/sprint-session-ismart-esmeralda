from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS 
from langchain.embeddings import OpenAIEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = OpenAIEmbeddings(openai_api_key = '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')

vector_store = FAISS.load_local('atendimento/faiss_index', embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_k = 2)

def junta_docs(docs):
    return '\n\n'.join([doc.page_content for doc in docs])

def get_prompt(query):

    return f"""Responda a query utilizando o contexto disponibilizado:
    Query: {query}

    Contexto:{junta_docs(retriever.invoke(query))}"""

