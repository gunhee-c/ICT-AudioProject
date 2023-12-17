import streamlit as st
import librosa as lr
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import io
import os
import requests

#TODO
"""
def convert_m4a_to_wav(m4a_path):
    
    Convert an M4A file to WAV format.

    wav_path = os.path.splitext(m4a_path)[0] + '.wav'
    audio = AudioSegment.from_file(m4a_path, format="m4a")
    audio.export(wav_path, format="wav")
    return wav_path
# 
"""

def play_librosa_audio(y, sr):
    # Convert the NumPy array to an audio buffer
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, y, sr, format='WAV')
    audio_buffer.seek(0)
    # Use st.audio to display the audio player
    st.audio(audio_buffer, format='audio/wav')
    
#
def show_waveform(audio, sr):
    fig, ax = plt.subplots()
    time = lr.samples_to_time(range(len(audio)), sr=sr)
    ax.plot(time, audio)
    ax.set(xlabel = 'Time (s)', ylabel = 'Sound Amplitude')
    plt.tight_layout()
    # Show plot in Streamlit
    st.pyplot(fig)

def show_spectrogram(audio, sr):
    fig, ax = plt.sublots()
    S = lr.feature.melspectrogram(y=audio, sr=sr)
    D = lr.power_to_db(S, ref=np.max)
    plt.figure(figsize=(10, 4))
    lr.display.specshow(D, sr=sr, y_axis='log', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-scaled spectrogram')
    plt.ylim(20, None)  # Set the y-axis range to be greater than 20
    plt.tight_layout()
    st.pyplot(fig)
    plt.show()

#c
def cut_audio(audio, sr, start_sec, end_sec):
    start_sample = int(start_sec * sr)
    end_sample = int(end_sec * sr)
    # Extract the desired segment
    segment = audio[start_sample:end_sample]
    return segment


#
def validate_start_end(full, start, end):
    if start < 0:
        st.error('Start time must be greater than 0')
        return False
    if end >= (full - 1):
        st.error('End time must be less than the duration of the audio file')
        return False
    if end - start > 30:
        st.error('Segment length must be less than or equal to 30 seconds')
        return False
    if end - start < 3:
        st.error('Segment length is to short: make it longer than 3 seconds')
        return False
    if start >= end:
        st.error('End time must be greater than start time')
        return False
    return True

###################################
def main_preprocess():


# URL of the raw audio file on GitHub
    audio_file_url = 'https://github.com/gunhee-c/ICT-AudioProject/blob/main/Sample_IR2.wav?raw=true'
    response = requests.get(audio_file_url)
    if response.status_code == 200:
        st.audio(response.content, format='audio/wav')
    else:
        st.write("Failed to load audio file.")
# Send a GET request to the URL

    # Header 적용
    st.header('Upload your Audio:')

    #uploaded_file = st.file_uploader("Choose a WAV file", type=["wav", "mp3", "m4a"])
    uploaded_file = st.file_uploader("Choose a WAV file")

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
        play_librosa_audio(audio_mono, sr)
        show_waveform(audio_mono, sr)
        st.write('Get your sample audio segment - under 30 seconds length')
        st.header('Now cut your sample ( 3 < sec < 30 ):')

        start_sample = st.number_input('From which second do you want to sample?')
        end_sample = st.number_input('To which second do you want to sample?')

        activate_sampler = False
        if st.button('Get your Sample!'):
            activate_sampler = validate_start_end(audio_length, start_sample, end_sample)
        
        if activate_sampler == True:
            st.success('Your sample length is legitimate.')
            audio_sample = cut_audio(audio_mono, sr, start_sample, end_sample)
            play_librosa_audio(audio_sample, sr)
            show_waveform(audio_sample, sr)  
    #[Audio_Original, Audio_Segment, sr, Audio_Length, Audio_Start, Audio_End, Boolean]
            
            return [audio_mono, audio_sample, sr, audio_length, activate_sampler]
