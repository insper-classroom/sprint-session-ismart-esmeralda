import streamlit as st 
import numpy as np
import openai
import requests
from raglogic import get_prompt
from classificador import classifier
import urllib.parse
from streamlit.web.server.websocket_headers import _get_websocket_headers
import os

st.image('documents\img\LOGO-ismart.png', width=100)
st.header('Tire suas dúvidas com seu assistente pessoal!')


openai.api_key = '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'


# Get the user's name from the URL
username = st.query_params.get('username', [''])

# Get the user's uuID from the URL
useruuid = st.query_params.get('useruuid', [''])



#se o modelo ainda n foi definido na sessao atual, cria uma chave no dicionario p ele
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = "gpt-3.5-turbo"

#se ainda n tiver nenhuma msg na sessao atual, cria uma lista vazia pguardar elas
if "messages" not in st.session_state:
    st.session_state.messages = []

    #mensagem inicial do bot, c o nome do usuario
    st.session_state.messages.append({'role': 'assistant', 'content': f'Olá, {username}! Sou a coruja, assistente virtual do Ismart. Como posso te ajudar hoje? Pode perguntar qualquer coisa! 🦉'})

if st.button('Ser atendido'):
    # tresmensagens = [message['content'] for message in st.session_state.messages if message['role'] == 'user']
    # concatenated_messages = ' '.join(tresmensagens)
    # tag = classifier(concatenated_messages)[0]

    # encoded_tags = urllib.parse.quote(tag)
    
    # #redirect to the url of the chatbot
    # webbrowser.open('wa.me/+14155238886')
    st.markdown("<a href='//wa.me/+14155238886' target='_self'> <img src='https://pngimg.com/d/whatsapp_PNG21.png' style=' width:5%; height:5%;'></a>", unsafe_allow_html=True)
    st.markdown("<a href='https://mail.google.com/mail/?view=cm&fs=1&to=ismart.contactmail@gmail.com&su=Tire%20Sua%20Dúvida' target='_self'> <img src='https://w7.pngwing.com/pngs/877/133/png-transparent-google-mail-logo-gmail-computer-icons-logo-email-gmail-angle-text-rectangle-thumbnail.png' style=' width:5%; height:5%;'> </a>", unsafe_allow_html=True)
   



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