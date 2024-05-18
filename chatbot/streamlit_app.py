import streamlit as st 
import numpy as np
import openai
from raglogic import get_prompt

st.title('Chatbot basico')

openai.api_key = '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'

display = []

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Digite sua dúvida...')
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
        display.append({'role': 'user', 'content': prompt})
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    augmentedprompt = get_prompt(prompt)

    messages_copy = st.session_state.messages.copy()
    messages_copy.append({'role': 'user', 'content': augmentedprompt})

    with st.chat_message('assistant', avatar = '🦉'):
        stream = openai.chat.completions.create(
            model = st.session_state['openai_model'],
            messages = [
                {"role": m["role"], "content": m["content"]} for m in messages_copy
            ],
            stream = True
        )
        response = st.write_stream(stream)
    display.append({'role': 'assistant', 'content': response})
    st.session_state.messages.append({"role": "assistant", "content": response})