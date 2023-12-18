import streamlit as st
import librosa as lr
import numpy as np

from Preprocess import *
from MainprocessForked import *
from TryMath import st_injection
from dialogue import *

def create_widget_set(key):
    opt = st.selectbox('Which effect will you choose: ', ["None", "I: Phone-effect", "E: Add air", "S: Reverb", "N: Compressor", 
                                   "F: Octave High", "T: Octave Low", "P: Noise Cancelling", "J: Autotune"], 
                                   key=f'select_{key}')
    rat = st.slider("Select a Value", min_value=0, max_value=100, key=f'slider_{key}')
    return [opt,rat]

def audio_visualize(data, sr, var):
    keyv = "toggle" + var
    keyr = "radio" + var
    var = st.toggle('Check your audio!', key = keyv)

    if var:
        play_librosa_audio(data, sr)
        vis = st.radio('View Your Audio Image:', ["none","Waveform", "Spectrogram" ], key=keyr)
        if vis == "none":
            st.write("Choose your Visualization mode")
        if vis == "Spectrogram":
            #st.write('View Audio Spectrogram')
            show_spectrogram(data, sr)
        elif vis == "Waveform":
            #st.write('View Audio Waveform')
            show_waveform(data, sr)



st.title('MBTI AUDIO EFFECTOR PROTOTYPE'':sunglasses:')
# URL of the raw audio file on GitHub
audio_file_url = 'https://github.com/gunhee-c/ICT-AudioProject/blob/main/Sample_IR2.wav?raw=true'
response = requests.get(audio_file_url)
if response.status_code == 200:
    st.audio(response.content, format='audio/wav')
else:
    st.write("Failed to load audio file.")

#Dummy Data
activate_sampler = False

tabFirst , tabSecond = st.tabs(["MBTI 보컬 이펙터?", "Upload your Audio"])

with tabFirst:

    tabFirst_message()

with tabSecond:

    st.header('Upload your Audio:')

    #uploaded_file = st.file_uploader("Choose a WAV file", type=["wav", "mp3", "m4a"])
    uploaded_file = st.file_uploader("Choose a WAV or MP3 file")

    if uploaded_file is not None:
        if (uploaded_file.type != "audio/wav") and (uploaded_file.type != "audio/x-m4a") and (uploaded_file.type != "audio/mpeg"):
            st.error("Please upload file that is wav, mp3, m4a format.")
        # Read the uploaded file
        st.success(uploaded_file.type)
        if uploaded_file.type == "audio/x-m4a":
            st.error("WOW YOU ARE TROLLING")
        audio_origin, sr = lr.load(uploaded_file, sr=None)
        audio_mono = lr.to_mono(audio_origin)
        audio_length = lr.get_duration(y = audio_mono, sr=sr)

        #How long is the audio
        st.write("Length of the original audio (Seconds): " + str(round(audio_length)) )
        #play_librosa_audio(audio_mono, sr)
        audio_visualize(audio_mono, sr, "audio_origin")
        #show_waveform(audio_mono, sr)
        st.write('Get your sample audio segment - under 30 seconds length')
        st.header('Now cut your sample ( 3 < sec < 30 ):')

        start_sample = st.number_input('From which second do you want to sample?')
        end_sample = st.number_input('To which second do you want to sample?')

        
        if button('Get your Sample!', key="button3"):
            activate_sampler = validate_start_end(audio_length, start_sample, end_sample)
        
    if activate_sampler == True:
        st.success('Your sample length is legitimate.')
        audio_sample = cut_audio(audio_mono, sr, start_sample, end_sample)
        #play_librosa_audio(audio_sample, sr)
        audio_visualize(audio_sample, sr, "audio_cut")
        main_data = [audio_mono, audio_sample, sr, audio_length, activate_sampler]  


if activate_sampler == False:
    st.header("먼저 샘플을 업로드 해주세요")

tab1, tab2, tab3 = st.tabs(["How to use", "Main", "Export"])

with tab1:
    tab1_message()

with tab2:
    
    chain_processed = False
    sr = main_data[2]
    audio_sample = main_data[1]
    audio_length = main_data[3]
    audio_mono = main_data[0]
    
    st.write("Combined Selectbox and Slider Widget")
    MBTIinput = []
    ratioinput = []
    numEffects = int(st.number_input('How many effects do you want to apply? max: 8', step=1))
    if numEffects == 0 or numEffects < 0:
        st.write("Choose at least one effect")
    elif numEffects > 9:
        st.write("Choose less than 9 effects")
    else:
        st.write("Choose your effects")
        index = 0
        for i in range(numEffects):
            ans = create_widget_set(index)
            MBTIinput.append(ans[0])
            ratioinput.append(ans[1])
            index += 1

        if st.button("Finished making Effector Chain"):
            chain_processed = True
            getAudio = phone(audio_sample, sr, 100)
            audio_visualize(getAudio, sr, "test")



with tab3:
    if chain_processed == False:
        st.write("Choose your effects first")
    else:
        for i in range(index):
            st.write(MBTIinput[i])
            st.write(ratioinput[i])
            st.write("")
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


#
