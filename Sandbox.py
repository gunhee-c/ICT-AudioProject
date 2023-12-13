import streamlit as st
import librosa as lr
import numpy as np

st.header('TESTING')

# Topbar categories
categories = ['Math', 'Audio', 'Information']
selected_category = st.sidebar.selectbox('Select a category', categories)

if selected_category == 'Math':
    # Add math-related code here
    st.write('Math category selected')
elif selected_category == 'Audio':
    # Add audio-related code here
    st.write('Audio category selected')
elif selected_category == 'Information':
    # Add information-related code here
    st.write('Information category selected')



