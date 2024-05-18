import tensorflow as tf
from langchain.embeddings import OpenAIEmbeddings 
import numpy as np

embeddings = OpenAIEmbeddings(openai_api_key = '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')

model = tf.keras.models.load_model('chatbot\classificacao.keras')

tags = {
    0: 'Sobre o Ismart',
    1: 'Ismart online',
    2: 'Processo seletivo',
    3: 'Bolsas de estudo',
}

def classifier(mensagens):
    embeded_input = np.array(embeddings.embed_documents(mensagens))

    prediction = model.predict(embeded_input, batch_size = 32)
    idx = np.argmax(prediction, axis = 1)
    return tags[idx[0]]

print(classifier(['O que é o Ismart?']))
