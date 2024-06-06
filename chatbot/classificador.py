import tensorflow as tf
from langchain.embeddings import OpenAIEmbeddings 
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

model = tf.keras.models.load_model('chatbot\classificacao.keras')

tags = {
    0: 'Sobre-o-Ismart',
    1: 'Ismart-online',
    2: 'Processo-seletivo',
    3: 'Bolsas-de-estudo',
}

def classifier(mensagem):
    embeded_input = np.array(embeddings.embed_documents([str(mensagem)]))

    prediction = model.predict(embeded_input, batch_size = 32)
    idx = np.argmax(prediction, axis = 1)
    idxs = np.argpartition(prediction, -2, axis = 1)
    return (tags[idxs[0][0]], tags[idxs[0][1]])

