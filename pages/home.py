import streamlit as st
import lorem
import pandas as pd
from millify import millify
def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Home</h1>", unsafe_allow_html=True)
    st.markdown("""
Welcome to the Home page of the European Aviation Analytics Dashboard. This webapplication is developed 
by <b>Quinten Goens</b>.""",unsafe_allow_html=True)
 

    df = pd.read_feather('resources/ASMA_Additional_Time.feather')
    col1,col2, col3, col4 = st.columns((1,1,1,4))
    FLT_2021 = df[df['YEAR']==2021]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2020 = df[df['YEAR']==2020]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2019 = df[df['YEAR']==2019]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2018 = df[df['YEAR']==2018]['FLT_ASMA_UNIMP_2'].sum()

    col1.metric("Inbound IFR flights 2019", millify(FLT_2019,precision=2), delta=round(((FLT_2019-FLT_2018)/FLT_2018)*100,2), delta_color="normal")
    col1.metric("Inbound IFR flights 2020", millify(FLT_2020,precision=2), delta=round(((FLT_2020-FLT_2019)/FLT_2019)*100,2), delta_color="normal")
    col1.metric("Inbound IFR flights 2021", millify(FLT_2021,precision=2), delta=round(((FLT_2021-FLT_2020)/FLT_2020)*100,2), delta_color="normal")

    ASMA_2021 = df[df['YEAR']==2021]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2020 = df[df['YEAR']==2020]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2019 = df[df['YEAR']==2019]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2018 = df[df['YEAR']==2018]['AVG_UNIMPEDED_ASMA_TIME'].median()

    col2.metric("Avg. unimp. ASMA time 2019 (median)", millify(ASMA_2019,precision=2), delta=round(((ASMA_2019-ASMA_2018)/ASMA_2018)*100,2), delta_color="normal")
    col2.metric("Avg. unimp. ASMA time 2020 (median)", millify(ASMA_2020,precision=2), delta=round(((ASMA_2020-ASMA_2019)/ASMA_2019)*100,2), delta_color="normal")
    col2.metric("Avg. unimp. ASMA time 2021 (median)", millify(ASMA_2021,precision=2), delta=round(((ASMA_2021-ASMA_2020)/ASMA_2020)*100,2), delta_color="normal")

    ASMA_ADD_2021 = df[df['YEAR']==2021]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2020 = df[df['YEAR']==2020]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2019 = df[df['YEAR']==2019]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2018 = df[df['YEAR']==2018]['AVG_ADDITIONAL_ASMA_TIME'].median()

    col3.metric("Avg. addit. ASMA time 2019 (median)", millify(ASMA_ADD_2019,precision=2), delta=round(((ASMA_ADD_2019-ASMA_ADD_2018)/ASMA_ADD_2018)*100,2), delta_color="normal")
    col3.metric("Avg. addit. ASMA time 2020 (median)", millify(ASMA_ADD_2020,precision=2), delta=round(((ASMA_ADD_2020-ASMA_ADD_2019)/ASMA_ADD_2019)*100,2), delta_color="normal")
    col3.metric("Avg. addit. ASMA time 2021 (median)", millify(ASMA_ADD_2021,precision=2), delta=round(((ASMA_ADD_2021-ASMA_ADD_2020)/ASMA_ADD_2020)*100,2), delta_color="normal")

    col4.markdown("""   
On this page, the HOME page, you can view some general metrics for the whole of Europe. More in depth metrics and visualizations can be found in the various pages of the application: 
* **ER DIAGRAM** - Entities and Relationships Diagram (Question 1).
* **QUERIES & VIEWS** - The various requested views and queries (Question 2).
* **AIRPORT AUTHORITY** - A dynamic dashboard including data visualizations for an airport authority (Question 3).
* **GENERAL PUBLIC** - A dynamic dashboard including data visualizations for the general public (Question 3).
* **NETWORK MANAGER** - A dynamic dashboard including data visualizations for a network manager (Question 3).
* **ABOUT** - About the application and the author incl. the technical tools used in the creation of this web app.

These can be navigated to by using the App Navigation dropdown in the left sidebar. If you encounter loading issues, please refresh and try again.""",unsafe_allow_html=True)

    st.markdown("""**Note:** Note that the <t style="color:#149414"><b>green</b></t> and <t style="color:#FF0000"><b>red</b></t> colored metrics (see above) indicate <t style="color:#149414"><b>increases</b></t>  or <t style="color:#FF0000"><b>decreases</b></t> relative to same metric the previous year. These metrics are Europe wide.""",unsafe_allow_html=True)
    
    