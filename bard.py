#DEPENDED LIBRARIES
import os
import easyocr
import streamlit as st
from PIL import Image
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

img = get_img_as_base64("media/BG_IMG.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image :url("data:media/png;base64,{img}");
background-size : cover;
}}
[data-testid="stHeader"]{{
background:rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("LET'S CHAT WITH SOME VOICES...!")
st.write("--------")

#HIDE MENU AND WATERMARK
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#CREATING VOICE OPTIONS IN SIDEBAR (elevenlabs voice options)
with st.sidebar:
    col1,col2=st.columns(2)
    with col1:
        st_lottie(lottie_json("media/AI.json"),speed=0.8, height=150, width=150,)
    with col2:
        st.title("Speech*2*Speech")
        st.title("CHATBOT")

    #CHAT MODEL SELECTION
    menu = ["ChatGPT - OpenAI","BardAI - Google","Siri - Apple","Llama - Meta/Facebook"]
    selected_menu = st.selectbox("Select Model", menu)
    
    #PROMPT TYPE SELECTION
    choice = ["SPEAK","TEXT","IMAGE"]
    selected_choice = st.selectbox("Select Choice", choice)


#PROCESS SPEECH TO TEXT TO SEARCH TO SPEECH
if selected_choice == "SPEAK":
    
    with st.sidebar:

        #SPEAKER SELECTION 
        voice_list = voices()
        voices = []
        for voice in voice_list:
            voices.append(voice.name)
        selected_voice = st.selectbox("Select voice", voices)
        SPEAK = st.button("Speak")
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
            AI_response_speech = bard(input_text)
            st.markdown(AI_response_speech)
            # if AI_response_speech:
            #     speech = text_to_speech(AI_response_speech, selected_voice, translation_mode)
            #     st.audio(speech)
        else:
            st.error("Please speak again..")


if selected_choice == "TEXT":
    PROMPT = st.text_input("Enter your prompt..",placeholder="Type your prompt here..")
    generate = st.button("Generate")
    if PROMPT and generate:
        AI_response_text = bard(PROMPT)
        if AI_response_text:
            st.markdown(f"**AI Response :**  {AI_response_text}")
    elif generate:
        st.info("Please Provide your prompt..!")


if selected_choice == "IMAGE":
    col1,col2 = st.columns(2)

    with col1:
    #UPLOAD IMAGE FILE
        image = st.file_uploader("Upload Image..", type=["png"])
    with col2:
        if image is not None:
            st.image(image,use_column_width=True)
        else:
            pass
    if image is not None:
        # CONVERT IMAGE TO PIL IMAGE
        pil_image = Image.open(image)

        # SAVING PIL IMAGE TO TEMPORARY FILE
        temp_image_path = "temp.png"
        pil_image.save(temp_image_path)

        model_path = "easyocr_model.pkl"
        reader = load_easyocr_model(model_path)

        # IMAGE TO TEXT EXTRACTION
        extracted_text = reader.readtext(temp_image_path)

        Explain = st.button("Explain")
        if extracted_text and Explain:
            extracted = []
            for item in extracted_text:
                extracted.append(item[1])
            AI_response_image = bard(" ".join(extracted))
            if AI_response_image:
                st.markdown(AI_response_image)  
                os.remove(temp_image_path)                  # DELETE TEMPORARY FILE IMAGE
        elif extracted_text is None:
            st.warning("No text found in the image.")

