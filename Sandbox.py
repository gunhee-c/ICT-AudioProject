import streamlit as st
import librosa as lr
import numpy as np

from MBTIVocalEffectProcess import main



st.header('TESTING')

main_preprocess()

tab1, tab2, tab3 = st.tabs(["메인", "Check ProgressSee Details", "MBTI 보컬 이펙터 설명"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



