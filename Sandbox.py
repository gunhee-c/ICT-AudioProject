import streamlit as st
import librosa as lr
import numpy as np
import tempfile
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
        vis = st.radio("Choose your Visualization mode", ["none","Waveform", "Spectrogram" ], key=keyr)
        if vis == "none":
            st.write("Audio Visualization: Disabled")
        if vis == "Spectrogram":
            #st.write('View Audio Spectrogram')
            show_spectrogram(data, sr)
        elif vis == "Waveform":
            #st.write('View Audio Waveform')
            show_waveform(data, sr)

def audio_expander(data, sr, var, text):

    keyr = "radio" + var
    with st.expander(text):
        play_librosa_audio(data, sr)
        vis = st.radio("Choose your Visualization mode", ["none","Waveform", "Spectrogram" ], key=keyr)
        if vis == "none":
            st.write("Audio Visualization: Disabled")
        if vis == "Spectrogram":
            #st.write('View Audio Spectrogram')
            show_spectrogram(data, sr)
        elif vis == "Waveform":
            #st.write('View Audio Waveform')
            show_waveform(data, sr)


def audio_processor(audio, sr, ratio, command, IR_audio, IR_sr):
    #st.write("Hello")
    if command == "I: Phone-effect":
        #st.write("Phone Effect on Action")
        return phone(audio, sr, ratio)
    if command == "E: Add air":
        #st.write("Air Effect on Action")
        return air(audio, sr, ratio)
    if command == "S: Reverb":
        #st.write("Reverb Effect on Action")
        return reverb(audio, sr, IR_audio, IR_sr, ratio)
    if command == "N: Compressor":
        #st.write("Compressor Effect on Action")
        return compressor(audio, sr, ratio)
    if command == "F: Octave High":
        #st.write("Octave High Effect on Action")
        return octHigh(audio, sr, ratio)
    if command == "T: Octave Low":
        #st.write("Octave Low Effect on Action")
        return octLow(audio, sr, ratio)
    if command == "P: Noise Cancelling":
        #st.write("Noise Cancelling Effect on Action")
        return noisereduce(audio, sr, ratio)
    if command == "J: Autotune":
        #st.write("Autotune Effect on Action")
        return autotune(audio, sr, ratio)


st.title('MBTI AUDIO EFFECTOR PROTOTYPE'':sunglasses:')
# URL of the raw audio file on GitHub
audio_file_url = 'https://github.com/gunhee-c/ICT-AudioProject/blob/main/Sample_IR.wav?raw=true'
response = requests.get(audio_file_url)
if response.status_code == 200:
    #st.audio(response.content, format='audio/wav')
    audio_buffer = io.BytesIO(response.content)

    # Load audio data with librosa
    IR_audio, IR_sr = lr.load(audio_buffer, sr=None)  
    IR_length = lr.get_duration(y = IR_audio, sr=IR_sr)
    #st.write(IR_length)
else:
    st.write("Failed to load audio file.")
#main_data= [1,1,1,1]

#Dummy Data
activate_sampler = False
get_final_result = False
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
        #audio_visualize(audio_mono, sr, "audio_origin")
        audio_expander(audio_mono, sr, "audio_origin", "원본 오디오:")
        #show_waveform(audio_mono, sr)
        st.write('Get your sample audio segment - under 30 seconds length')
        st.header('Now cut your sample ( 3 < sec < 30 ):')

        start_sample = st.number_input('From which second do you want to sample?')
        end_sample = st.number_input('To which second do you want to sample?')

        
        #if st.button('Get your Sample!', key="button3"):
        activate_sampler = validate_start_end(audio_length, start_sample, end_sample)
        
    if activate_sampler == True:
        st.success('Your sample length is legitimate.')
        audio_sample = cut_audio(audio_mono, sr, start_sample, end_sample)
        #play_librosa_audio(audio_sample, sr)
        audio_expander(audio_sample, sr, "audio_cut", "오디오 샘플:")
        #main_data = [audio_mono, audio_sample, sr, audio_length]  


if activate_sampler == False:
    st.header("먼저 샘플을 업로드 해주세요")

tab1, tab2, tab3, tab4 = st.tabs(["How to use", "Main", "See Progress", "Export"])

with tab1:
    tab1_message()

with tab2:
    
    chain_processed = False
    


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
        agree = st.checkbox("Finished making Effector Chain")
        if agree:
            st.write('Great!')
            chain_processed = True
            index = numEffects



with tab3:
    if chain_processed == False:
        st.write("Choose your effects first")
    else:
        st.write("Check your Effector Chain step by step:")
        #audio_print = [audio_sample]
        current_audio = audio_sample

        audio_expander(current_audio, sr, "audioSampleProgress0", "샘플 원본:")
        st.write("")
        st.write("")
        for i in range(index):
            #st.write("MBTIinput[i]:" + MBTIinput[i] + " ratioinput[i]:" + str(ratioinput[i]))
            if MBTIinput[i] != "None":
                processed_audio = audio_processor(current_audio, sr, ratioinput[i], MBTIinput[i], IR_audio, IR_sr)
                normalize(processed_audio, sr, 0.5)
                progstr = ("Process #" + str(i+1) + ": " + MBTIinput[i] + " Ratio: " + str(ratioinput[i]))

                    #audio_visualize(processed_audio, sr, f"audioSampleProgress{i+1}")
                audio_expander(processed_audio, sr, f"audioSampleProgress{i+1}", progstr)
                #processed_audio = processed_audio.squeeze() 
                
                #audio_visualize(processed_audio, sr, f"audioSampleProgress{i+1}")
                current_audio = processed_audio
                st.write("")
        
        st.write("The Audio below is your final result")
        current_audio = normalize(current_audio, sr, 1)

        audio_expander(current_audio, sr, "audioSampleProgressFinal", "최종 결과(샘플):")
#       
        satisfied = st.checkbox("Are you Satisfied with the result?")
        if satisfied:
            st.success("Great! Go to the next tab and export your audio")
            get_final_result = True
        else:
            st.error("You can go back to the previous tab and change the effects")

with tab4:
    if get_final_result == False:
        st.header("Please confirm your audio chain first.")
    if get_final_result == True:
        st.header("Start Exporting your audio")
        fin = st.checkbox("Let's do it!")
        if fin == True:
            st.write("Processing...")
            current_audio_final = audio_mono

            for i in range(index):
                if MBTIinput[i] != "None":
                    processed_audio_final = audio_processor(current_audio_final, sr, ratioinput[i], MBTIinput[i], IR_audio, IR_sr)
                    normalize(processed_audio_final, sr, 0.5)
                    current_audio_final = processed_audio_final
            Final_audio = normalize(current_audio_final, sr, 1)
            st.write("Export your audio")

            audio_expander(Final_audio, sr, "audioProgressFinal", "최종 결과(전체):")
        
            st.write("Do you wish to Download?")

            download = st.checkbox("Download")

            if download:
                output_file = 'output_audio.wav'
                sf.write(output_file, Final_audio, sr)
                st.write("Downloading...")


                with open(output_file, "rb") as file:
                    btn = st.download_button(
                                                label="Download Audio",
                                                data=file,
                                                file_name="processed_audio.wav",
                                                mime="audio/mpeg"
                                            )

                
                st.write("Download Complete!")
                st.write("Thank you for using our service!")
                st.balloons()