import streamlit as st
import lorem
import pandas as pd
import numpy as np

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Airport Authority Dashboard</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown("""
    Welcome to the Airport Authority dashboard. 
    
    Please select which Airport Authority you are working with (default: Brussels). If you want more information about the underlying data, please check out the ABOUT page.
    """)
    df = pd.read_feather('resources/ASMA_Additional_Time.feather')

    APT_NAME = col2.selectbox('Airport Authority', df['APT_NAME'].unique())

    if pd.isnull(APT_NAME):
        APT_NAME='Brussels'

    df = pd.read_feather('resources/ASMA_Additional_Time.feather')

    def change_column_names(df):
        df.rename({
        'YEAR':'Year',
        'MONTH_MON':'Month',
        'CHANGE_MONTH':'Period (months)',
        'CHANGE_YEAR':'Period (years)',
        'FLT_ASMA_UNIMP_2':'IFR flights with unimpeded reference time',
        'AVG_UNIMPEDED_ASMA_TIME':'Avg. unimpeded ASMA time',
        'AVG_ADDITIONAL_ASMA_TIME':'Avg. additional ASMA time',
        'CHANGE_AVG_UNIMPEDED_ASMA_TIME':'Pct. change in avg. unimpeded ASMA time',
        'CHANGE_AVG_ADDITIONAL_ASMA_TIME':'Pct. change in avg. additional ASMA time',
        }, axis=1, inplace=True)
        return df
    



    