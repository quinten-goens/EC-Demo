import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import home
from pages import airport_authority,general_public, network_manager, about
from random import randint

st.set_page_config(page_title = "Analytics Dashboard", page_icon = "🌐", layout = "wide", theme='light')

c4_header, c1_header, c3_header= st.columns((1,1,1))
st.sidebar.image("resources/header.png",use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center; color: black;'>European Aviation Analytics</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: black;'>Developed by Q. Goens</h3>", unsafe_allow_html=True)

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("HOME", home.app)
app.add_page("AIRPORT AUTHORITY", airport_authority.app)
app.add_page("GENERAL PUBLIC", general_public.app)
app.add_page("NETWORK MANAGER", network_manager.app)
app.add_page("ABOUT", about.app)

# The main app
app.run()
if 'key' not in st.session_state: 
    st.session_state.key = str(randint(1000, 100000000))

st.sidebar.info("This is a demo of a Streamlit dashboard designed for EUROCONTROL in view of the application process for the position of Performance Data Analyst. See the ABOUT page for more information.")
