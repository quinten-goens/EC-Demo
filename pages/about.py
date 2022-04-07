import streamlit as st
import lorem

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>About</h1>", unsafe_allow_html=True)
    st.markdown(lorem.paragraph())

    if st.button("Balloons"):
        st.balloons()