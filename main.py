import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import home
from pages import example_page1,example_page2, about
from random import randint

st.set_page_config(page_title = "Streamlit Template Dashboard", page_icon = "🌐", layout = "wide")

c4_header, c1_header, c3_header= st.columns((1,1,1))

st.sidebar.markdown("<h1 style='text-align: center; color: black;'>Streamlit Template Dashboard</h1>", unsafe_allow_html=True)


# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("HOME", home.app)
app.add_page("EXAMPLE PAGE 1", example_page1.app)
app.add_page("EXAMPLE PAGE 2", example_page2.app)
app.add_page("ABOUT", about.app)

# The main app
app.run()
if 'key' not in st.session_state: 
    st.session_state.key = str(randint(1000, 100000000))