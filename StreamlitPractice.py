import streamlit as st
import librosa as lr
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import io



# 
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

st.title('MBTI AUDIO EFFECTOR PROTOTYPE'':sunglasses:')


# Header 적용
st.header('Upload your Audio:')

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav", "mp3", "m4a"])


if uploaded_file is not None:
    # Read the uploaded file
    audio_origin, sr = lr.load(uploaded_file, sr=None)
    audio_mono = lr.to_mono(audio_origin)
    audio_length = lr.get_duration(y = audio_mono, sr=sr)

    #How long is the audio
    st.write("Length of the original audio (Seconds): " + str(round(audio_length)) )
    play_librosa_audio(audio_mono, sr)
    show_waveform(audio_mono, sr)
    st.write('Get your sample audio segment - under 30 seconds length')
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
"""
    # Plotting the waveform
    S = lr.feature.melspectrogram(y = audio_mono, sr=sr)
    
    # Convert to log scale (dB)
    D = lr.power_to_db(S, ref=np.max)
    
    # Display the spectrogram
    plt.figure(figsize=(10, 4))
    lr.display.specshow(D, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-scaled spectrogram')
    plt.tight_layout()
    st.pyplot(plt)
"""
# Subheader 적용
st.subheader('이것은 subheader 입니다')

# 캡션 적용
st.caption('캡션을 한 번 넣어 봤습니다')

# 코드 표시
sample_code = '''
def function():
    print('hello, world')
'''
st.code(sample_code, language="python")


"""
# 일반 텍스트
st.text('일반적인 텍스트를 입력해 보았습니다.')

# 마크다운 문법 지원
st.markdown('streamlit은 **마크다운 문법을 지원**합니다.')
# 컬러코드: blue, green, orange, red, violet
st.markdown("텍스트의 색상을 :green[초록색]으로, 그리고 **:blue[파란색]** 볼트체로 설정할 수 있습니다.")
st.markdown(":green[$\sqrt{x^2+y^2}=1$] 와 같이 latex 문법의 수식 표현도 가능합니다 :pencil:")

# LaTex 수식 지원
st.latex(r'\sqrt{x^2+y^2}=1')
"""
