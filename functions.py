#DEPENDED LIBRARIES
import os
import json
import easyocr
import base64
import pickle
from bardapi import Bard
import speech_recognition as sr
from elevenlabs import generate
from dotenv import load_dotenv


#SETTING API KEY ENVIRONMENTS
load_dotenv()
bard_key = os.environ.get("_BARD_API_KEY")


#TO OPEN IMAGE BACKGROUND
def get_img_as_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#TO RENDER LOTTIE JSON FILE
def lottie_json(path:str):
    with open(path) as f:
        return json.load(f)
    
#BARD AI SEARCH RESULT (BardAI API function to search) 
def bard(input_text):
    prompt = f'{input_text}  in short'
    result = ((Bard().get_answer(input_text=prompt)['content']))
    return result

#GENERATE TEXT TO SPEECH (elevenlabs API function for text to speech)
def text_to_speech(text, voice_name, translation_mode):
    audio = generate(text=text, voice=voice_name,model=translation_mode)
    return audio

#GETTING AUDIO FROM MICROPHONE AND CONVERTING INTO TEXT (google speech recognition)
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text

#TO SAVE EASCYOCR AS PICKEL FILE
def save_easyocr_model(model_path, languages):
    reader = easyocr.Reader(languages)
    with open(model_path, 'wb') as f:
        pickle.dump(reader, f)

#TO LOAD PICKEL OCR MODEL
def load_easyocr_model(model_path):
    with open(model_path, 'rb') as f:
        reader = pickle.load(f)
    return reader