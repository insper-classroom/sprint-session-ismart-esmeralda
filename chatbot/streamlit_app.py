import streamlit as st 
import numpy as np
import openai
import requests
from raglogic import get_prompt
import urllib.parse
from streamlit.web.server.websocket_headers import _get_websocket_headers
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

st.image('documents\img\LOGO-ismart.png', width=100)
st.header('Tire suas dúvidas com seu assistente pessoal!')


openai.api_key = OPENAI_API_KEY


# Pega o nome do usuário da URL
username = st.query_params.get('username', [''])

# Se o modelo ainda não tiver sido definido, define o modelo como gpt-3.5-turbo
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = "gpt-3.5-turbo"

#Se a variavel state messages nao existir, cria ela
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Se o nome do usuário não estiver vazio, adiciona uma mensagem de boas-vindas
    st.session_state.messages.append({'role': 'assistant', 'content': f'Olá, {username}! Sou a coruja, assistente virtual do Ismart. Como posso te ajudar hoje? Pode perguntar qualquer coisa! 🦉'})

# Faz com que apareça os botões que encaminham o usuário para o whatsapp ou email
if st.button('Ser atendido'):

    st.markdown("<a href='//wa.me/+14155238886' target='_self'> <img src='https://pngimg.com/d/whatsapp_PNG21.png' style=' width:5%; height:5%;'></a>", unsafe_allow_html=True)
    st.markdown("<a href='https://mail.google.com/mail/?view=cm&fs=1&to=ismart.contactmail@gmail.com&su=Tire%20Sua%20Dúvida' target='_self'> <img src='https://w7.pngwing.com/pngs/877/133/png-transparent-google-mail-logo-gmail-computer-icons-logo-email-gmail-angle-text-rectangle-thumbnail.png' style=' width:5%; height:5%;'> </a>", unsafe_allow_html=True)
   


#mostra as mensagens
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Digite sua dúvida...')
# Se o usuário digitar algo, envia a mensagem para o modelo
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    augmentedprompt = get_prompt(prompt)

    # Adiciona a mensagem do usuário à lista de mensagens
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