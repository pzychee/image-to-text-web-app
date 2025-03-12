#======================== IMPORT PACKAGES ===========================

import numpy as np
import matplotlib.pyplot as plt 
from tkinter.filedialog import askopenfilename
import tifffile as tiff
#import cv2 
import matplotlib.image as mpimg
import base64
import streamlit as st
from gtts import gTTS
import warnings

 

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# ================ Background image ===

st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:36px;">{"Photo to Text Converter App for the Visually Impaired"}</h1>', unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('b.jpg')

#========================  INPUT IMAGE===========================


st.write("--------------------------------------------------------------------------------------------------")


file_upload = st.file_uploader("Upload Image",['png','jpg'])

if file_upload is None:
    
    st.text("Kindly Upload input Image")

else:
    
    img = mpimg.imread(file_upload)
    
    
    st.image(img,caption='Input Image')
    
    st.write("----------------------------------------------------------------------------")
    
    
    #============================ 4.TEXT EXTRACTION ====================
    
    
    import pytesseract 
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    trans_text = pytesseract.image_to_string(img,lang = 'eng')
    
    
    print()
    print("----------------------------------------------")
    print(" EXTRACTED TEXT")
    print("----------------------------------------------")
    print()
    print(trans_text)
    
    st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:24px;">{"Extracted Text"}</h1>', unsafe_allow_html=True)

    st.write("-------------------------------------------------")
    
    st.write(trans_text)
    
    st.write("---------------------------------------------------------------------------------------")

    
    # ----------------------------------------- TEXT TRANSLATION
    
    st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:28px;">{"Text Translation"}</h1>', unsafe_allow_html=True)

    
    from googletrans import Translator, LANGUAGES

    # Define language options
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())
    
    # Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Source language selection
        src_language = st.selectbox("Source Language", language_names, index=language_names.index('english'))
        src_language_code = language_codes[language_names.index(src_language)]
        
        # Save source language to file
        try:
            with open('source.txt', 'w') as file2:
                file2.write(src_language_code)
        except Exception as e:
            st.error(f"Error writing source language to file: {e}")
        
        # Input text area
        
        st.write(trans_text)
        
        
        
        if st.button("Submit"):
            # Save input text to file
            try:
                with open('inputtext.txt', 'w') as file1:
                    file1.write(trans_text)
            except Exception as e:
                st.error(f"Error writing input text to file: {e}")
    
    with col2:
        # Destination language selection
        dest_language = st.selectbox("Destination Language", language_names, index=language_names.index('spanish'))
        dest_language_code = language_codes[language_names.index(dest_language)]
        
        try:
            # Read source language code from file
            with open('source.txt', 'r') as file11:
                src_language_code = file11.read().strip()
            
            # Read input text from file
            with open('inputtext.txt', 'r') as file1:
                input_text = file1.read().strip()
        except Exception as e:
            st.error(f"Error reading from file: {e}")
            src_language_code = ""
            input_text = ""
    
        # Debugging statements
        # st.write(f"Source Language Code: {src_language_code}")
        # st.write(f"Input Text: {input_text}")
    
    
        # Translate text
        if src_language_code and dest_language_code:
            
            
            from deep_translator import GoogleTranslator

            # Text to be translated
            text_to_translate = trans_text

            # Translate to Spanish (es)
            translated_text = GoogleTranslator(source=src_language_code, target=dest_language_code).translate(text_to_translate)
            
            
            
            
            # translated_text = translate_text(similar_sentence, src_language_code, dest_language_code)
            st.text_area("", value=translated_text, height=200, disabled=True)
        else:
            st.text_area("", value="Translation could not be performed. Check inputs and try again.", height=200, disabled=True)
    
        
        
        
    st.write("---------------------------------------------------------------------------------------")
        
        
    # ---------------------------- SPEECH TRANSLATION ----------------------------------------
    
    st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:28px;">{"Speech Translation"}</h1>', unsafe_allow_html=True)

    
    
    speech_language_names = list(LANGUAGES.values())
    speech_language_codes = list(LANGUAGES.keys())
    
    
    # Allow the user to choose a language for speech
    speech_lang = st.selectbox("Choose Speech Language", speech_language_names, index=speech_language_names.index(dest_language))
    speech_lang_code = speech_language_codes[speech_language_names.index(speech_lang)]
    
    # # Convert the translated text to speech using gTTS
    # if st.button("Convert to Speech"):
    #     tts = gTTS(text=trans_text, lang=speech_lang_code, slow=False)
    #     speech_file = "translated_speech.mp3"
    #     tts.save(speech_file)
        
    #     # Provide the option to download the speech file
    #     st.audio(speech_file, format="audio/mp3")
        
    #     st.download_button(label="Download Speech", data=open(speech_file, 'rb').read(), file_name="translated_speech.mp3")
        
    if st.button("Convert to Speech"):
        # Make sure we use the translated text for speech conversion
        tts = gTTS(text=translated_text, lang=speech_lang_code, slow=False)
        speech_file = "translated_speech.mp3"
        tts.save(speech_file)
        
        # Provide the option to download the speech file
        st.audio(speech_file, format="audio/mp3")
        
        st.download_button(label="Download Speech", data=open(speech_file, 'rb').read(), file_name="translated_speech.mp3")