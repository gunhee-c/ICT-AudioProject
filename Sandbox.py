import streamlit as st
import librosa as lr
import numpy as np

from TryMath import st_injection

st.header('TESTING')

# Topbar categories
categories = ['Math', 'Audio', 'Information']
selected_category = st.sidebar.selectbox('Select a category', categories)

if selected_category == 'Math':
    st_injection()
elif selected_category == 'Audio':
    # Add audio-related code here
    st.write('Audio category selected')
elif selected_category == 'Information':
    # Add information-related code here
    st.write('Information category selected')



