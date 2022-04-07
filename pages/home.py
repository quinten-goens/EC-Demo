import streamlit as st
import lorem

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Home</h1>", unsafe_allow_html=True)

    col1,col2, col3, col4 = st.columns((1,1,1,4))
    col1.markdown('**Statistics**')
    
    col1.metric(
        "Metric One",
        "551,000", "12%")

    col1.metric(
        "Metric Two",
        "4,500", "5%")

    col1.metric(
        "Metric Three",
        "3,200", "19%")
    
    col2.markdown("**Countersigned contracts**")
    col2.metric(
        "Metric Four",
        "1,215", "12%")
    col2.metric(
        "Metric Five",
        "778", "12%")
    col2.metric(
        "Metric Six",
        "1.10", "12%")

    col3.markdown("**⠀⠀**")
    col3.metric(
        "Metric Seven",
        "1,215", "2%")
    
    col3.metric(
        "Metric Eight",
        "8.44", "55%")
    col3.metric(
        "Metric Nine",
        "1.10", "42%")
    

    col4.markdown(lorem.paragraph())

    st.markdown(lorem.paragraph())
    
    
    
    