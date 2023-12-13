import streamlit as st
import librosa as lr
import numpy as np

from Preprocess import *
from TryMath import st_injection

tabFirst , tabSecond = st,tabs(["MBTI 보컬 이펙터 설명", "Upload your Audio"])

with tabFirst:
    st.title('MBTI AUDIO EFFECTOR PROTOTYPE'':sunglasses:')
    st.header('MBTI 보컬 이펙터 설명')
    st.write('MBTI 컨셉을 이용해 당신의 보컬 소리에 이펙트를 넣어보세요')
    st.write('당신의 보컬을 더욱 더 멋지게 만들어줄 것입니다')
with tabSecond:
    a = main_preprocess()
    st.write(a)    

tab1, tab2, tab3 = st.tabs(["메인", "Check ProgressSee Details", "MBTI 보컬 이펙터 설명"])

with tab1:
    st_injection()

    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



