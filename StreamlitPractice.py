import streamlit as st
import librosa as lr
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import io

# Copied from tutorial
# 타이틀 적용 예시

#def

#
st.title(':sunglasses:''MBTI AUDIO EFFECTOR PROTOTYPE'':sunglasses:')


# Header 적용
st.header('Upload your Audio:')

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav", "mp3", "m4a"])


if uploaded_file is not None:
    # Read the uploaded file
    audio_origin, sr = lr.load(uploaded_file, sr=None)


    # Plotting the waveform
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio_origin, sr=sr)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()

    st.pyplot(plt)

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
