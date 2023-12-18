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
    fig, ax = plt.subplots(figsize=(10, 3))
    time = lr.samples_to_time(range(len(audio)), sr=sr)
    ax.plot(time, audio)
    ax.set(xlabel = 'Time (s)', ylabel = 'Sound Amplitude')
    plt.tight_layout()
    # Show plot in Streamlit
    st.pyplot(fig)
"""
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
"""

def show_spectrogram(audio, sr):
    # Compute the spectrogram
    S = np.abs(lr.stft(audio))

    # Convert to dBs
    dB = lr.amplitude_to_db(S, ref=np.max)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 3))
    img = lr.display.specshow(dB, sr=sr, x_axis='time', y_axis='log', ax=ax)
    ax.set(title='Spectrogram')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")

    # Show the plot in Streamlit
    st.pyplot(fig)

#c
def cut_audio(audio, sr, start_sec, end_sec):
    start_sample = int(start_sec * sr)
    end_sample = int(end_sec * sr)
    # Extract the desired segment
    segment = audio[start_sample:end_sample]

    
    fade_duration = 0.01  # Fade duration in seconds, e.g., 10ms
    fade_length = int(fade_duration * sr)  # Convert fade duration to number of samples

    # Apply fade-in
    fade_in = np.linspace(0, 1, fade_length)
    segment[:fade_length] *= fade_in

    # Apply fade-out
    fade_out = np.linspace(1, 0, fade_length)
    segment[-fade_length:] *= fade_out
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

