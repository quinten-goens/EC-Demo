import streamlit as st
import lorem
import pandas as pd
import numpy as np
import plotly.express as px

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Airport Authority Dashboard</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown("""
    **Welcome to the Airport Authority dashboard.** 
    
    The aim of this dashboard is to provide you some **insight in to IFR flight statistics and relevant ASMA time (unimpeded and additional) for your relevant airport authority.** Please select which Airport Authority you are working with (default: Brussels). 
    
    For more information about the underlying data and the developer of this platform, please check out the ABOUT page.
    """)

    df = pd.read_feather('resources/ASMA_Additional_Time.feather')

    col2.markdown("""### Please select an airport authority""")
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

    st.markdown('## IFR flight statistics')
    col3, col4 = st.columns(2)
    @st.cache(allow_output_mutation=True)
    def make_fig1(APT_NAME):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = df_tmp.groupby('YEAR').sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp = change_column_names(df_tmp)

        fig = px.line(df_tmp, x='Year', y='IFR flights with unimpeded reference time', title='Total IFR flights with unimpeded reference time for ' + APT_NAME)
        fig.layout.yaxis=dict(title='Yearly total IFR flights with unimpeded reference time')
        return fig
    
    col3.plotly_chart(make_fig1(APT_NAME), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig2(APT_NAME):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = change_column_names(df_tmp)
        fig = px.line(df_tmp, x='Month', y='IFR flights with unimpeded reference time', title='IFR flights with unimpeded reference time over time in ' + APT_NAME,color='Year')
        return fig
    
    col4.plotly_chart(make_fig2(APT_NAME), use_container_width=True)
    
    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graphs above provides information about the number of inbound IFR (Instrument Flight Rules) flights with unimpeded reference time for a selected airport authority. The unimpeded reference time is the time it takes for a flight to reach the airport and be cleared for departure. 
        
        The left graph shows yearly total IFR flights whereas the right one shows monthly totals for various years.

        ### Interpretation
        Both graphs indicate for various airport authorities a significant decrease in flights in 2020, this is the effect of [Covid-19 and the lock-down restrictions](https://en.wikipedia.org/wiki/COVID-19). A specific note is to be made for the airport authority Brussels: In 2016 a significant dip in flights is noticable around March and April 2016. This likely is caused by the [2016 Brussels Bombings](https://en.wikipedia.org/wiki/2016_Brussels_bombings).  
        """)

    st.markdown('## Annual ASMA time flight statistics')
    col5, col6 = st.columns(2)
    @st.cache(allow_output_mutation=True)
    def make_fig3(APT_NAME):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = df_tmp.groupby('YEAR').mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()

        df_tmp = change_column_names(df_tmp)

        fig = px.bar(df_tmp, x='Year', y=['Avg. unimpeded ASMA time','Avg. additional ASMA time'], title='Average ASMA Time for ' + APT_NAME  )
        fig.layout.yaxis=dict(title='Avg. ASMA Time (minutes)')
        return fig
    
    col5.plotly_chart(make_fig3(APT_NAME), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig4(APT_NAME):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = df_tmp.groupby('YEAR').mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()

        df_tmp['CHANGE_AVG_UNIMPEDED_ASMA_TIME'] = df_tmp['AVG_UNIMPEDED_ASMA_TIME'].pct_change()*100
        df_tmp['CHANGE_AVG_ADDITIONAL_ASMA_TIME'] = df_tmp['AVG_ADDITIONAL_ASMA_TIME'].pct_change()*100
        df_tmp['CHANGE_YEAR'] = df_tmp['YEAR'].apply(lambda l: f"{l-1}-{l}")

        df_tmp = change_column_names(df_tmp)

        df_tmp = df_tmp[~df_tmp['Pct. change in avg. unimpeded ASMA time'].isna()]
        fig = px.bar(df_tmp, x='Period (years)', y=['Pct. change in avg. unimpeded ASMA time','Pct. change in avg. additional ASMA time'], title='Percentage change (%) of average ASMA Time per year for ' + APT_NAME  )
        fig.layout.yaxis=dict(title='Pct. change (%)')
        return fig
    
    col6.plotly_chart(make_fig4(APT_NAME), use_container_width=True)
    
    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graphs above provide information and insight in the average unimpeded ASMA time and the average additional ASMA time for a selected airport authority. ASMA stands for Arrival Sequencing and Metering Area and is often defined as a vertical column around the relevant airport with a radius of 40 [NM](https://en.wikipedia.org/wiki/Nautical_mile). ASMA entry time is the time the flight enters the area within 40 NM radius around the airport and the Actual Landing Time is denoted as ALDT. The additional ASMA time is the difference between the actual ASMA transit time and the median unimpeded ASMA transit time for the group of similar flights. The ASMA additional time for the airport is the average of the average ASMA values for all flights. 
        
        The left graph shows average (unimpeded and additional) ASMA time per year whereas the right one shows the percentage change in a certain period for various years.

        *Note: Clicking the legend allows you to disable the corresponding graph and can enhance the visualization.* 

        ### Interpretation
        A large percentual increase of the avg. unimpeded ASMA time from 2019 to 2020 for various authorities indicates the potential impact of [Covid-19 and the lock-down restrictions](https://en.wikipedia.org/wiki/COVID-19).  
        """)
    st.markdown('## Monthly ASMA time flight statistics')
    col7_, col8_ = st.columns(2)
    col7_.markdown('This section allows to view more granular data on the monthly level. Please select the year of interest.')
    YEAR = col8_.selectbox('Year of Interest', df['YEAR'].unique())
    
    col7, col8 = st.columns(2)
    @st.cache(allow_output_mutation=True)
    def make_fig5(APT_NAME,YEAR):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = df[df['YEAR'] == YEAR]
        df_tmp = df_tmp.groupby(['MONTH_MON','MONTH_NUM']).mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_tmp = df_tmp.sort_values('MONTH_NUM')

        df_tmp = change_column_names(df_tmp)

        fig = px.bar(df_tmp, x='Month', y=['Avg. unimpeded ASMA time','Avg. additional ASMA time'], title='Average ASMA Time for ' + APT_NAME +' in ' + str(YEAR))
        fig.layout.yaxis=dict(title='Avg. ASMA Time (minutes)')
        return fig
    
    col7.plotly_chart(make_fig5(APT_NAME,YEAR), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig6(APT_NAME, YEAR):
        df_tmp = df[df['APT_NAME'] == APT_NAME]
        df_tmp = df[df['YEAR'] == YEAR]
        df_tmp = df_tmp.groupby(['MONTH_MON','MONTH_NUM']).mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_tmp = df_tmp.sort_values('MONTH_NUM')

        df_tmp['CHANGE_AVG_UNIMPEDED_ASMA_TIME'] = df_tmp['AVG_UNIMPEDED_ASMA_TIME'].pct_change()*100
        df_tmp['CHANGE_AVG_ADDITIONAL_ASMA_TIME'] = df_tmp['AVG_ADDITIONAL_ASMA_TIME'].pct_change()*100

        transl = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC', 0:'DEC'}

        df_tmp['CHANGE_MONTH'] = df_tmp['MONTH_NUM'].apply(lambda l: f"{transl[l-1]}-{transl[l]}")

        df_tmp = change_column_names(df_tmp)

        df_tmp = df_tmp[~df_tmp['Pct. change in avg. unimpeded ASMA time'].isna()]
        fig = px.bar(df_tmp, x='Period (months)', y=['Pct. change in avg. unimpeded ASMA time','Pct. change in avg. additional ASMA time'], title='Percentage change (%) of average ASMA Time per Month for ' + APT_NAME +' in ' + str(YEAR)  )
        fig.layout.yaxis=dict(title='Pct. change (%)')
        return fig
    
    col8.plotly_chart(make_fig6(APT_NAME,YEAR), use_container_width=True)

    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graphs above provide information and insight in the average unimpeded ASMA time and the average additional ASMA time for a selected airport authority. ASMA stands for Arrival Sequencing and Metering Area and is often defined as a vertical column around the relevant airport with a radius of 40 [NM](https://en.wikipedia.org/wiki/Nautical_mile). ASMA entry time is the time the flight enters the area within 40 NM radius around the airport and the Actual Landing Time is denoted as ALDT. The additional ASMA time is the difference between the actual ASMA transit time and the median unimpeded ASMA transit time for the group of similar flights. The ASMA additional time for the airport is the average of the average ASMA values for all flights. 
        
        The left graph shows average (unimpeded and additional) ASMA time per month for the selected year whereas the right one shows the percentage change in a certain period for various months for the selected year.

        *Note: Clicking the legend allows you to disable the corresponding graph and can enhance the visualization.* 

        ### Interpretation
        No specific interpretations to be made.  
        """)
    