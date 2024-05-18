import streamlit as st 
import numpy as np
import openai
from raglogic import get_prompt
import urllib.parse

st.title('Chatbot basico')

openai.api_key = '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'


# Get the user's name from the URL
username = st.query_params.get('username', [''])

# Get the user's ID from the URL
userid = st.query_params.get('userid', [''])

#se o modelo ainda n foi definido na sessao atual, cria uma chave no dicionario p ele
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = "gpt-3.5-turbo"

#se ainda n tiver nenhuma msg na sessao atual, cria uma lista vazia pguardar elas
if "messages" not in st.session_state:
    st.session_state.messages = []

#mensagem inicial do bot, c o nome do usuario
st.session_state.messages.append({'role': 'assistant', 'content': f'Olá, {username}! Sou a coruja, assistente virtual aqui do Ismart. Como posso te ajudar hoje? Pode perguntar qualquer coisa! 🦉'})

#mostra as mensagens guardadas na variavel state messages
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Digite sua dúvida...')
#se o prompt nao estiver vazio, mostra a mensagem dele e puxa o rag
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    augmentedprompt = get_prompt(prompt)

    # cria uma copia pra mandar pro modelo c o prompt do rag, p n mostrar o prompt do rag pro usuario
    messages_copy = st.session_state.messages.copy()
    messages_copy.append({'role': 'user', 'content': augmentedprompt})

    #resposta do llm
    with st.chat_message('assistant', avatar = '🦉'):
        stream = openai.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [
                {"role": m["role"], "content": m["content"]} for m in messages_copy
            ],
            stream = True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})