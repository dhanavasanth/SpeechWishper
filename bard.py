#DEPENDED LIBRARIES
import os
import streamlit as st
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
from elevenlabs import set_api_key,voices


#IMPORTING FUNCTIONS
from functions import *


#SETTING API KEY ENVIRONMENTS 
load_dotenv()
api_key = os.environ.get("api_key")
set_api_key(api_key)

#MULTI-LANGUAGE MODEL                           #  | SINGLE LANGUAGE MODEL('en')
translation_mode = "eleven_multilingual_v1"     #  | "eleven_monolingual_v1"

#CONFIGURING STREAMLIT WEBPAGE
st.set_page_config(page_title="S2S-CHATBOT", page_icon=":speech_balloon:")
st.title("LET'S CHAT WITH SOME VOICES")
st.write("--------")


#CREATING VOICE OPTIONS IN SIDEBAR (elevenlabs voice options)
with st.sidebar:
    col1,col2=st.columns(2)
    with col1:
        st_lottie(lottie_json("media/AI.json"),speed=0.8, height=150, width=150,)
    with col2:
        st.title("Speech*2*Speech")
        st.title("CHATBOT")

    #CHATBOT SELECTION
    menu = ["ChatGPT - OpenAI","BardAI - Google","Siri - Apple","Llama - Meta/Facebook"]
    selected_menu = st.selectbox("Select Model", menu)
    
    #SPEAKER SELECTION 
    voice_list = voices()
    voices = []
    for voice in voice_list:
        voices.append(voice.name)
    selected_voice = st.selectbox("Select voice", voices)
    SPEAK = st.button("Speak")


#PROCESS SPEECH TO TEXT TO SEARCH TO SPEECH
if SPEAK:
    col1,col2,col3 = st.columns(3)

    #LOAD LOTTIE ANIMATION FILE
    with col1:
        if selected_menu == "ChatGPT - OpenAI":
            st.image("media/chatgpt_img.png",width=150)
        if selected_menu == "Siri - Apple": 
            st.lottie(lottie_json("media/siri.json"),height=150,width=300,speed=0.8,loop=True)
        if selected_menu == "BardAI - Google": 
            st.lottie(lottie_json("media/google.json"),height=200,width=300,speed=0.8,loop=True)
        if selected_menu == "Llama - Meta/Facebook": 
            st.lottie(lottie_json("media/llama.json"),height=200,width=300,speed=0.8,loop=True)

    #GETTING AUDIO FROM MICROPHONE
    with col2:
        st.title("I'm listening...")
        try:
            input_text = get_audio()
        except UnboundLocalError:
            input_text = None
    if input_text is not None:
        st.subheader(f'Your Prompt: {input_text} ..?')
    #     AI_response = bard(input_text)
    #     st.subheader(AI_response)
    #     if AI_response:
    #         speech = text_to_speech(AI_response, selected_voice, translation_mode)
    #         st.audio(speech)
    else:
        st.error("Please speak again")





