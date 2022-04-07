import streamlit as st
import lorem
import pandas as pd
import numpy as np
import plotly.express as px

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

    APT_NAME = 'Brussels'
    df_tmp = df[df['APT_NAME'] == APT_NAME]
    df_tmp = df_tmp.groupby('YEAR').sum()['FLT_ASMA_UNIMP_2'].reset_index()

    df_tmp = change_column_names(df_tmp)

    fig1 = px.line(df_tmp, x='Year', y='IFR flights with unimpeded reference time', title='Total IFR flights with unimpeded reference time for ' + APT_NAME)
    fig1.layout.yaxis=dict(title='Yearly total IFR flights with unimpeded reference time')
    
    st.plotly_chart(fig1)
    



    