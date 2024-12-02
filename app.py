import streamlit as st
from openai import OpenAI
import pandas as pd
import os

os.environ['OPENAI_API_KEY'] = 'INSERT_API_KEY'

client = OpenAI()

def obtener_respuesta_openai(prompt, df_string=None):
    if df_string:
        messages = [
            {"role": "system", "content": "You are a data analyst. Here is the data:\n" + df_string},
            {"role": "user", "content": prompt}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    
    return response.choices[0].message.content.strip()

# Función para generar una imagen con DALL·E
def generar_imagen(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

# Función para generar audio
def generar_audio(prompt):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=prompt
    )
    audio_file_path = "output.mp3"
    response.stream_to_file(audio_file_path)
    
    return audio_file_path

# Interfaz Streamlit
st.title("Wilo-Chatbot con OpenAI")

# Cargar archivo CSV
file = st.file_uploader("Carga una tabla CSV", type="csv")
if file is not None:
    df = pd.read_csv(file)
    st.write("Tabla Cargada:")
    st.write(df.head())
    
    # Convertir el DataFrame a string para pasarlo al modelo
    df_string = df.to_string()    
    st.write("Ingresa una pregunta relacionada con los datos.")
    
    # Entrada de texto del usuario
    prompt = st.text_input("Escribe tu pregunta:")
    if prompt:
        respuesta = obtener_respuesta_openai(prompt, df_string)
        st.write(respuesta)
else:
    # Entrada de texto sin tabla
    prompt = st.text_input("Escribe un mensaje:")
    if prompt:
        respuesta = obtener_respuesta_openai(prompt)
        st.write(respuesta)

# Opciones adicionales para generar imagen o audio
st.write("Opciones adicionales:")
generar_imagen_button = st.button("Generar Imagen con DALL·E")
generar_audio_button = st.button("Generar Audio desde el texto")

if generar_imagen_button and prompt:
    imagen_url = generar_imagen(prompt)
    st.image(imagen_url, use_column_width=True)

if generar_audio_button and prompt:
    audio = generar_audio(prompt)
    st.audio(audio, format="audio/mp3")
