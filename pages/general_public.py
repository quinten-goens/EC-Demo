import streamlit as st
import lorem

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Example page 1</h1>", unsafe_allow_html=True)
    st.markdown(lorem.paragraph())

    