import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

# Custom imports 
from multipage import MultiPage
from pages import home
from pages import er_diagram,queries_views,airport_authority,general_public, network_manager, about
from random import randint

st.set_page_config(page_title = "Analytics Dashboard", page_icon = "✈️", layout = "wide")

c4_header, c1_header, c3_header= st.columns((1,1,1))
st.sidebar.image("resources/header.png",use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center; color: black;'>European Aviation Analytics</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: black;'>Developed by Q. Goens</h3>", unsafe_allow_html=True)

# Create an instance of the app 
app = MultiPage()

# Add all your applications (pages) here
app.add_page("HOME", home.app)
app.add_page("ER DIAGRAM", er_diagram.app)
app.add_page("QUERIES & VIEWS", queries_views.app)
app.add_page("AIRPORT AUTHORITY", airport_authority.app)
app.add_page("GENERAL PUBLIC", general_public.app)
app.add_page("NETWORK MANAGER", network_manager.app)
app.add_page("ABOUT", about.app)

# The main app
app.run()
if 'key' not in st.session_state: 
    st.session_state.key = str(randint(1000, 100000000))

st.sidebar.info("""
This web application is a demo of a European Aviation Analytics dashboard designed for EUROCONTROL in view of the application process.

For information about the application and its' future releases and improvements see the ABOUT page. 
""")

st.sidebar.markdown("""
<sub><sup>Version: 0.0.3 (Last updated: 18 April 2022)</sup></sub>""", unsafe_allow_html=True)
#def to_excel():
#    df = pd.read_feather('resources/ASMA_Additional_Time.feather')
#    output = BytesIO()
#    writer = pd.ExcelWriter(output, engine='xlsxwriter')
#    df.to_excel(writer, index=False, sheet_name='Sheet1')
#    workbook = writer.book
#    worksheet = writer.sheets['Sheet1']
#    format1 = workbook.add_format({'num_format': '0.00'}) 
#    worksheet.set_column('A:A', None, format1)  
#    writer.save()
##    processed_data = output.getvalue()
#    return processed_data

#df_xlsx = to_excel()
#st.sidebar.download_button(label='📥 Download Raw Data', data=df_xlsx, file_name= 'ASMA_Additional_Time.xlsx')