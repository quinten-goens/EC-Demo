import streamlit as st
import lorem
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import plotly.express as px
import json
import urllib.request
import pickle


def app():
    st.markdown("<h1 style='text-align: left; color: black;'>General Public Dashboard</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown("""
    Welcome to the general public dashboard. 
    
    The aim of this dashboard is to provide you some insight in to popularity of various flight destinations and the impact of the Covid-19 on European aviation. 
    
    For more information about the underlying data and the developer of this platform, please check out the ABOUT page.
    """)

    df = pd.read_feather('resources/ASMA_Additional_Time.feather')

    col1.markdown("""### Select parameters of interest
    """) 
    col1.markdown("Please select a destination country (or countries) and a time period which you are interested in to learn more about.")
    flight_destinations = col1.multiselect('Destination countries of interest', default = ['Malta','Belgium','Netherlands','Portugal'],options=list(df['STATE_NAME'].unique()))

    try:
        if pd.isnull(flight_destinations):
            flight_destinations = ['Brussels', 'Malta', 'Netherlands', 'Greece'] 
    except:
        pass


    start_period = col1.date_input(
     "Start period of interest ",
     datetime(2016,1,1))
    
    end_period = col1.date_input(
     "End period of interest ",
     datetime(2019,12,31))

    def change_column_names(df):
        df.rename({
        'YEAR':'Year',
        'MONTH_MON':'Month',
        'CHANGE_MONTH':'Period (months)',
        'CHANGE_YEAR':'Period (years)',
        'DATE':'Date',
        'APT_NAME':'Airport name',
        'STATE_NAME':'Country in which the airport of arrival is located',
        'FLT_ASMA_UNIMP_2':'IFR flights with unimpeded reference time',
        'CHANGE_FLT_ASMA_UNIMP_2':'Pct. change in IFR flights with unimpeded reference time',
        'AVG_UNIMPEDED_ASMA_TIME':'Avg. unimpeded ASMA time',
        'AVG_ADDITIONAL_ASMA_TIME':'Avg. additional ASMA time',
        'CHANGE_AVG_UNIMPEDED_ASMA_TIME':'Pct. change in avg. unimpeded ASMA time',
        'CHANGE_AVG_ADDITIONAL_ASMA_TIME':'Pct. change in avg. additional ASMA time',
        }, axis=1, inplace=True)
        return df

    @st.cache(allow_output_mutation=True)
    def map_graph():
        fig_inbound_increase = open("resources/fig_inbound_total.pkl", "rb")
        fig = pickle.load(fig_inbound_increase)
        fig_inbound_increase.close()
        return fig
    
    col2.plotly_chart(map_graph(), use_container_width=True)
    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graph in the top right corner provides information about the number of inbound IFR (Instrument Flight Rules) flights with unimpeded reference time for all European countries in 2021. The unimpeded reference time is the time it takes for a flight to reach the airport and be cleared for departure. 
        
        The graph shows total IFR flights in 2021.

        ### Interpretation
        Spain had the most inbound IFR flights in 2021 (around 467k flights) followed up by Germany (around 428k flights) and France (around 314k flights).
        """)
    st.markdown('## Relative popularity of selected flight destinations by country and airport')
    col3, col4 = st.columns(2)
    
    @st.cache(allow_output_mutation=True)
    def make_fig1(flight_destinations, start_period, end_period):
        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp = change_column_names(df_tmp)

        fig = px.line(df_tmp,x='Date',y='IFR flights with unimpeded reference time',color='Country in which the airport of arrival is located',title='Number of IFR flights with unimpeded reference time per destination')
        fig = fig.update_xaxes(range=[start_period,end_period])
        return fig
    
    col3.plotly_chart(make_fig1(flight_destinations, start_period, end_period), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig2(flight_destinations, start_period, end_period):
        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME', 'APT_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp = change_column_names(df_tmp)

        fig = px.line(df_tmp,x='Date',y='IFR flights with unimpeded reference time',color='Country in which the airport of arrival is located',line_dash='Airport name',title='Number of IFR flights with unimpeded reference time per destination and airport')
        fig.update_xaxes(range=[start_period,end_period])
        return fig
    
    col4.plotly_chart(make_fig2(flight_destinations, start_period, end_period), use_container_width=True)
    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graph above provides information about the number of inbound IFR (Instrument Flight Rules) flights with unimpeded reference time for the selected European countries in over time. The unimpeded reference time is the time it takes for a flight to reach the airport and be cleared for departure. 
        
        The left graph shows total IFR flights for each country over time whereas the right graph does the same but for each airport in the selected countries.

        ### Interpretation
        In both graphs a strong seasonality can be noted in most (if not all) countries and airports. The increase of flights in the summer period is related with the holiday period.
        """)
    st.markdown('## Impact of COVID-19 on European aviation (Covid-19 data: ECDC)')
    st.markdown('### Total IFR flights for Europe')
    

    col5a, col6a = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def make_fig3a():
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df.groupby(['DATE']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp = change_column_names(df_tmp)

        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='IFR flights with unimpeded reference time',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the number of IFR flights with unimpeded reference time in Europe")
        fig.update_yaxes(title_text="IFR flights with unimpeded reference time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig
        
    col5a.plotly_chart(make_fig3a(), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig4a():
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df.groupby(['DATE']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp['CHANGE_FLT_ASMA_UNIMP_2']= df_tmp['FLT_ASMA_UNIMP_2'].pct_change()*100

        df_tmp = change_column_names(df_tmp)

        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Pct. change in IFR flights with unimpeded reference time',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the number of IFR flights with unimpeded reference time in Europe")
        fig.update_yaxes(title_text="Pct. change in IFR flights (reference: prev. month)", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col6a.plotly_chart(make_fig4a(), use_container_width=True)

    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graph above provides information about the number of inbound IFR (Instrument Flight Rules) flights with unimpeded reference time for Europe over time with a specific emphasis on the [Covid-19](https://en.wikipedia.org/wiki/Covid-19) period. The unimpeded reference time is the time it takes for a flight to reach the airport and be cleared for departure. 
        
        The left graph shows total IFR flights for Europe over time during the covid-19 period whereas the right graph shows percentual changes relative to the same metric the month earlier.

        ### Interpretation
        In both graphs a strong seasonality can be noted in Europe, this is linked due to the holiday period in which more people travel. A decrease of the number of flights with about a factor 10 can be noted during the Covid-19 period.
        """)

    st.markdown('### IFR flights for selected countries')

    col5, col6 = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def make_fig3(flight_destinations):
    
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        df_tmp = change_column_names(df_tmp)


        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='IFR flights with unimpeded reference time',color='Country in which the airport of arrival is located',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination")
        fig.update_yaxes(title_text="IFR flights with unimpeded reference time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig
        
    col5.plotly_chart(make_fig3(flight_destinations), use_container_width=True)

    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graph above provides information about the number of inbound IFR (Instrument Flight Rules) flights with unimpeded reference time for the selected countries over time with a specific emphasis on the [Covid-19](https://en.wikipedia.org/wiki/Covid-19) period. The unimpeded reference time is the time it takes for a flight to reach the airport and be cleared for departure. 
        
        The left graph shows total IFR flights for the selected countries over time during the covid-19 period whereas the right graph shows percentual changes relative to the same metric the month earlier. On both graphs a logarithmic bar chart indicates the daily Covid-19 cases in Europe (source data: ECDC).

        ### Interpretation
        In both graphs a strong seasonality can be noted in most (if not all) selected countries, this is linked due to the holiday period in which more people travel. A decrease of the number of flights with about a factor 10 can be noted during the Covid-19 period (i.e. the period in which the number of cases skyrockets).
        """)

    @st.cache(allow_output_mutation=True)
    def make_fig4(flight_destinations):
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()

        dfs = []
        for x in df_tmp['STATE_NAME'].unique():
            tmp = df_tmp[df_tmp['STATE_NAME']==x]
            tmp['CHANGE_FLT_ASMA_UNIMP_2']= tmp['FLT_ASMA_UNIMP_2'].pct_change()*100
            dfs.append(tmp)
        df_tmp = pd.concat(dfs)

        df_tmp = change_column_names(df_tmp)

        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Pct. change in IFR flights with unimpeded reference time',color='Country in which the airport of arrival is located',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination")
        fig.update_yaxes(title_text="Pct. change in IFR flights (reference: prev. month)", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col6.plotly_chart(make_fig4(flight_destinations), use_container_width=True)

    st.markdown('### Average ASMA time for Europe')

    col7a, col8a = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def make_fig5a():
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df.groupby(['DATE']).mean()['AVG_UNIMPEDED_ASMA_TIME'].reset_index()

        df_tmp = change_column_names(df_tmp)


        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Avg. unimpeded ASMA time',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time in Europe').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the avg. unimpeded ASMA time in Europe")
        fig.update_yaxes(title_text="Avg. unimpeded ASMA time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col7a.plotly_chart(make_fig5a(), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig6a():
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df.groupby(['DATE']).mean()['AVG_ADDITIONAL_ASMA_TIME'].reset_index()

        df_tmp = change_column_names(df_tmp)


        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Avg. additional ASMA time',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time in Europe').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the avg. additional ASMA time in Europe")
        fig.update_yaxes(title_text="Avg. additional ASMA time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col8a.plotly_chart(make_fig6a(), use_container_width=True)

    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graphs above provide information and insight in the average unimpeded ASMA time and the average additional ASMA time for Europe. ASMA stands for Arrival Sequencing and Metering Area and is often defined as a vertical column around the relevant airport with a radius of 40 [NM](https://en.wikipedia.org/wiki/Nautical_mile). ASMA entry time is the time the flight enters the area within 40 NM radius around the airport and the Actual Landing Time is denoted as ALDT. The additional ASMA time is the difference between the actual ASMA transit time and the median unimpeded ASMA transit time for the group of similar flights. The ASMA additional time for the airport is the average of the average ASMA values for all flights. 
        
        The left graph shows average unimpeded ASMA time over time whereas the right one shows the average additional ASMA time over time. On both graphs a logarithmic bar chart indicates the daily Covid-19 cases in Europe (source data: ECDC). 
 
        ### Interpretation
        An overall increase of avg. unimpeded ASMA time can be noted over time, this increase accellerated during the Covid-19 outbreak. The average additional ASMA decreases over time and dives down during Covid-19. Likely this phenomenom is related to the decrease in the number of flights leading to shorter queuing times and thus shorter additional ASMA times.""")
        

    st.markdown('### ASMA time for selected countries')

    col7, col8 = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def make_fig5(flight_destinations):
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME']).mean()['AVG_UNIMPEDED_ASMA_TIME'].reset_index()

        df_tmp = change_column_names(df_tmp)


        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Avg. unimpeded ASMA time',color='Country in which the airport of arrival is located',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the avg. unimpeded ASMA time per destination")
        fig.update_yaxes(title_text="Avg. unimpeded ASMA time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col7.plotly_chart(make_fig5(flight_destinations), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig6(flight_destinations):
        start_period = datetime(2017,1,1)
        end_period = datetime(2022,1,1)

        df_tmp = df[df['STATE_NAME'].isin(flight_destinations)]

        df_tmp = df_tmp.groupby(['DATE', 'STATE_NAME']).mean()['AVG_ADDITIONAL_ASMA_TIME'].reset_index()

        df_tmp = change_column_names(df_tmp)


        c19 = pd.read_feather('resources/covid-daily-cases.feather') # https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Bar(x=c19['date'],y=c19['cases'],name='Covid-19 cases',opacity=0.5),secondary_y=True)
        fig.add_traces(
            list(px.line(df_tmp,x='Date',y='Avg. additional ASMA time',color='Country in which the airport of arrival is located',title='Impact of Covid-19 on the number of IFR flights with unimpeded reference time per destination').select_traces()
        ))

        fig.update_xaxes(range=[start_period,end_period])
        # update title
        fig.update_layout(title_text="Impact of Covid-19 on the avg. additional ASMA time per destination")
        fig.update_yaxes(title_text="Avg. additional ASMA time", secondary_y=False)
        fig.update_yaxes(title_text="Daily Covid-19 Cases in Europe (logarithmic)", secondary_y=True,type="log")
        return fig

    col8.plotly_chart(make_fig6(flight_destinations), use_container_width=True)

    with st.expander('Additional information and interpretation'):
        st.markdown("""
        ### Additional information
        The graphs above provide information and insight in the average unimpeded ASMA time and the average additional ASMA time for the selected countries. ASMA stands for Arrival Sequencing and Metering Area and is often defined as a vertical column around the relevant airport with a radius of 40 [NM](https://en.wikipedia.org/wiki/Nautical_mile). ASMA entry time is the time the flight enters the area within 40 NM radius around the airport and the Actual Landing Time is denoted as ALDT. The additional ASMA time is the difference between the actual ASMA transit time and the median unimpeded ASMA transit time for the group of similar flights. The ASMA additional time for the airport is the average of the average ASMA values for all flights. 
        
        The left graph shows average unimpeded ASMA time over time whereas the right one shows the average additional ASMA time over time. On both graphs a logarithmic bar chart indicates the daily Covid-19 cases in Europe (source data: ECDC). 
 
        ### Interpretation
        An overall increase of avg. unimpeded ASMA time can be noted over time, this increase accellerated during the Covid-19 outbreak. The average additional ASMA decreases over time and dives down during Covid-19. Likely this phenomenom is related to the decrease in the number of flights leading to shorter queuing times and thus shorter additional ASMA times.""")

