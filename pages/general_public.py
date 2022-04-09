import streamlit as st
import lorem
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import plotly.express as px
import json
import urllib.request


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
    col1.markdown("Please select which destination country (or countries) and a time period which you are interested in to learn more about.")
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
        countries = pd.read_feather('resources/countries.feather')
        EU_url = 'https://gist.githubusercontent.com/phil-pedruco/10447085/raw/426fb47f0a6793776a044f17e66d17cbbf8061ad/countries.geo.json'
        def read_geojson(url):
            with urllib.request.urlopen(url) as url:
                jdata = json.loads(url.read().decode())
            return jdata 
        
        jdata = read_geojson(EU_url)
        YEAR = 2021
        df_tmp = df[df['YEAR']==YEAR]
        df_tmp = df_tmp.groupby(['YEAR','STATE_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()
        df_tmp = df_tmp.merge(countries,left_on='STATE_NAME', right_on='country_names', how='left')

        fig= go.Figure(go.Choroplethmapbox(z=df_tmp['FLT_ASMA_UNIMP_2'].to_list(), # This is the data.
                                    locations=df_tmp['locations'].to_list(),
                                    colorscale='reds',
                                    colorbar=dict(thickness=20, ticklen=3),
                                    geojson=jdata,
                                    text=df_tmp['STATE_NAME'].to_list(),
                                    hoverinfo='all',
                                    marker_line_width=1, marker_opacity=0.75))
                                    
                                    
        fig.update_layout(title_text= f'Number of IFR flights in {YEAR} per country',width = 700,height=700,
                        mapbox = dict(center= dict(lat=54.5260,  lon=15.2551),
                                        style='carto-positron',
                                        zoom=2.4,
                                    ));
        return fig
    
    col2.plotly_chart(map_graph(), use_container_width=True)
    
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
