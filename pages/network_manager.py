import streamlit as st
import lorem
import pandas as pd
from millify import millify
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit as st
import pickle
import plotly.express as px

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

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Network Manager Dashboard</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    col1.markdown("""
    **Welcome to the Network Manager Dashboard.** 
    
    The aim of this dashboard is to **provide monitoring over time for the various countries and airport authorities for a network manager.** For more information about the underlying data and the developer of this platform, please check out the ABOUT page.
    """)
    df = pd.read_feather('resources/ASMA_Additional_Time.feather')
    col1.markdown("""The metrics on the right hand side are Europe wide. Note that the <t style="color:#149414"><b>green</b></t> and <t style="color:#FF0000"><b>red</b></t> colored metrics indicate <t style="color:#149414"><b>increases</b></t>  or <t style="color:#FF0000"><b>decreases</b></t> relative to same metric the previous year.""", unsafe_allow_html=True)
    col1.markdown("""<b>Note: As a network manager you might be interested in using the raw data. You can download the raw data here:</b>""",unsafe_allow_html=True)
    df_xlsx = to_excel(df)
    col1.download_button(label='📥 Download Raw Data', data=df_xlsx, file_name= 'ASMA_Additional_Time.xlsx')
    
    FLT_2021 = df[df['YEAR']==2021]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2020 = df[df['YEAR']==2020]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2019 = df[df['YEAR']==2019]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2018 = df[df['YEAR']==2018]['FLT_ASMA_UNIMP_2'].sum()

    col2.metric("Inbound IFR flights 2019", millify(FLT_2019,precision=2), delta=round(((FLT_2019-FLT_2018)/FLT_2018)*100,2), delta_color="normal")
    col2.metric("Inbound IFR flights 2020", millify(FLT_2020,precision=2), delta=round(((FLT_2020-FLT_2019)/FLT_2019)*100,2), delta_color="normal")
    col2.metric("Inbound IFR flights 2021", millify(FLT_2021,precision=2), delta=round(((FLT_2021-FLT_2020)/FLT_2020)*100,2), delta_color="normal")

    ASMA_2021 = df[df['YEAR']==2021]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2020 = df[df['YEAR']==2020]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2019 = df[df['YEAR']==2019]['AVG_UNIMPEDED_ASMA_TIME'].median()
    ASMA_2018 = df[df['YEAR']==2018]['AVG_UNIMPEDED_ASMA_TIME'].median()

    col3.metric("Avg. unimp. ASMA time 2019 (median)", millify(ASMA_2019,precision=2), delta=round(((ASMA_2019-ASMA_2018)/ASMA_2018)*100,2), delta_color="normal")
    col3.metric("Avg. unimp. ASMA time 2020 (median)", millify(ASMA_2020,precision=2), delta=round(((ASMA_2020-ASMA_2019)/ASMA_2019)*100,2), delta_color="normal")
    col3.metric("Avg. unimp. ASMA time 2021 (median)", millify(ASMA_2021,precision=2), delta=round(((ASMA_2021-ASMA_2020)/ASMA_2020)*100,2), delta_color="normal")

    ASMA_ADD_2021 = df[df['YEAR']==2021]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2020 = df[df['YEAR']==2020]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2019 = df[df['YEAR']==2019]['AVG_ADDITIONAL_ASMA_TIME'].median()
    ASMA_ADD_2018 = df[df['YEAR']==2018]['AVG_ADDITIONAL_ASMA_TIME'].median()

    col4.metric("Avg. addit. ASMA time 2019 (median)", millify(ASMA_ADD_2019,precision=2), delta=round(((ASMA_ADD_2019-ASMA_ADD_2018)/ASMA_ADD_2018)*100,2), delta_color="normal")
    col4.metric("Avg. addit. ASMA time 2020 (median)", millify(ASMA_ADD_2020,precision=2), delta=round(((ASMA_ADD_2020-ASMA_ADD_2019)/ASMA_ADD_2019)*100,2), delta_color="normal")
    col4.metric("Avg. addit. ASMA time 2021 (median)", millify(ASMA_ADD_2021,precision=2), delta=round(((ASMA_ADD_2021-ASMA_ADD_2020)/ASMA_ADD_2020)*100,2), delta_color="normal")

    st.markdown("## Airport performance overview")
    st.markdown("""This section provides an **overview of the best and worst performers within the network w.r.t. ASMA time**. Select a year of interest and the number of best / worst performers you want to have displayed.""")
    col5b,col6b = st.columns(2)
    YEAR = col5b.selectbox("Year of interest", [2014,2015, 2016,2017,2018,2019,2020,2021])
    TOP = col6b.slider("Number of best / worst performers to display", min_value=1, max_value=47, value=10)

    st.markdown('#### Unimpeded ASMA time')
    col5aa,col6aa = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def get_top_performers_avg_unimp(YEAR,TOP):
        # Best performers in the year 2016 for AVG unimmpeded ASMA time
        df_tmp = df.groupby(['APT_NAME','YEAR']).mean()['AVG_UNIMPEDED_ASMA_TIME'].reset_index()
        df_tmp = df_tmp[df_tmp['YEAR']==YEAR]
        df_tmp.sort_values('AVG_UNIMPEDED_ASMA_TIME', ascending=True, inplace=True)
        df_tmp = df_tmp.head(TOP)
        df_tmp = change_column_names(df_tmp)
        fig = px.bar(df_tmp, x='Airport name', y='Avg. unimpeded ASMA time', title=f'Top {TOP} best performers in the year ' + str(YEAR) + ' for avg. unimpeded ASMA time (best:left)')
        return fig
    
    col5aa.plotly_chart(get_top_performers_avg_unimp(YEAR,TOP))

    @st.cache(allow_output_mutation=True)
    def get_worst_performers_avg_unimp(YEAR,TOP):
        df_tmp = df.groupby(['APT_NAME','YEAR']).mean()['AVG_UNIMPEDED_ASMA_TIME'].reset_index()
        df_tmp = df_tmp[df_tmp['YEAR']==YEAR]
        df_tmp.sort_values('AVG_UNIMPEDED_ASMA_TIME', ascending=False, inplace=True)
        df_tmp = df_tmp.head(TOP)
        df_tmp.sort_values('AVG_UNIMPEDED_ASMA_TIME', ascending=True, inplace=True)
        df_tmp = change_column_names(df_tmp)
        fig = px.bar(df_tmp, x='Airport name', y='Avg. unimpeded ASMA time', title=f'Top {TOP} worst performers in the year ' + str(YEAR) + ' for avg. unimpeded ASMA time (worst: right)')
        return fig
    
    col6aa.plotly_chart(get_worst_performers_avg_unimp(YEAR,TOP))
    st.markdown('#### Additional ASMA time')
    col5aaa,col6aaa = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def get_top_performers_avg_add(YEAR,TOP):
        df_tmp = df.groupby(['APT_NAME','YEAR']).mean()['AVG_ADDITIONAL_ASMA_TIME'].reset_index()
        df_tmp = df_tmp[df_tmp['YEAR']==YEAR]
        df_tmp.sort_values('AVG_ADDITIONAL_ASMA_TIME', ascending=True, inplace=True)
        df_tmp = df_tmp.head(TOP)
        df_tmp = change_column_names(df_tmp)
        fig = px.bar(df_tmp, x='Airport name', y='Avg. additional ASMA time', title=f'Top {TOP} best performers in the year ' + str(YEAR) + ' for avg. additional ASMA time (best:left)')
        return fig
    
    col5aaa.plotly_chart(get_top_performers_avg_add(YEAR,TOP))

    @st.cache(allow_output_mutation=True)
    def get_worst_performers_avg_add(YEAR,TOP):
        df_tmp = df.groupby(['APT_NAME','YEAR']).mean()['AVG_ADDITIONAL_ASMA_TIME'].reset_index()
        df_tmp = df_tmp[df_tmp['YEAR']==YEAR]
        df_tmp.sort_values('AVG_ADDITIONAL_ASMA_TIME', ascending=False, inplace=True)
        df_tmp = df_tmp.head(TOP)
        df_tmp.sort_values('AVG_ADDITIONAL_ASMA_TIME', ascending=True, inplace=True)
        df_tmp = change_column_names(df_tmp)
        fig = px.bar(df_tmp, x='Airport name', y='Avg. additional ASMA time', title=f'Top {TOP} worst performers in the year ' + str(YEAR) + ' for avg. additional ASMA time (worst: right)')
        return fig
    
    col6aaa.plotly_chart(get_worst_performers_avg_add(YEAR,TOP))

    st.markdown('## Geographical Overview for 2021')
    col5, col6 = st.columns(2)
    
    @st.cache(allow_output_mutation=True)
    def make_fig1():
        fig_inbound_increase = open("resources/fig_inbound_total.pkl", "rb")
        fig = pickle.load(fig_inbound_increase)
        fig_inbound_increase.close()
        return fig
    
    col5.plotly_chart(make_fig1(), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig2():
        fig_inbound_increase = open("resources/fig_inbound_increase.pkl", "rb")
        fig = pickle.load(fig_inbound_increase)
        fig_inbound_increase.close()
        return fig
    
    col6.plotly_chart(make_fig2(), use_container_width=True)
    
    @st.cache(allow_output_mutation=True)
    def make_fig3():
        fig_inbound_increase = open("resources/fig_inbound_asma_unimp_incr.pkl", "rb")
        fig = pickle.load(fig_inbound_increase)
        fig_inbound_increase.close()
        return fig
    
    col5.plotly_chart(make_fig3(), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig4():
        fig_inbound_increase = open("resources/fig_inbound_asma_add_incr.pkl", "rb")
        fig = pickle.load(fig_inbound_increase)
        fig_inbound_increase.close()
        return fig
    
    col6.plotly_chart(make_fig4(), use_container_width=True)

    st.markdown("""
### Network Manager Comparison Tool (NMCT)
This tool allows the network manager to compare two airports' performance in various fields. 
##### Please select the airports you would like to compare
If you'd like to compare to the European reference, please select "Europe (Reference)" in the dropdown.""")
    col7_,col8_ = st.columns(2)
    AIRPORT1 = col7_.selectbox("Airport 1", ['Europe (Reference)'] + list(df['APT_NAME'].unique()))
    AIRPORT2 = col8_.selectbox("Airport 2", ['Europe (Reference)'] + list(df['APT_NAME'].unique()),index=1)
    st.markdown('##### Comparative IRF flight statistics')
    col7,col8 = st.columns(2)
    @st.cache(allow_output_mutation=True)
    def make_fig5(AIRPORT1,AIRPORT2):
        df_europe_ref = df.groupby('YEAR').sum()['FLT_ASMA_UNIMP_2'].reset_index()
        df_europe_ref['APT_NAME'] = 'Europe (Reference)'
        
        df_tmp = df.groupby(['YEAR','APT_NAME']).sum()['FLT_ASMA_UNIMP_2'].reset_index()
        df_tmp = pd.concat([df_tmp,df_europe_ref])

        df_tmp = df_tmp[df_tmp['APT_NAME'].isin([AIRPORT1, AIRPORT2])]

        df_tmp = change_column_names(df_tmp)

        fig = px.line(df_tmp, x='Year', y='IFR flights with unimpeded reference time', color='Airport name', title='Total IFR flights with unimpeded reference time comparison')
        fig.layout.yaxis=dict(title='Yearly total IFR flights with unimpeded reference time')
        return fig
    col7.plotly_chart(make_fig5(AIRPORT1,AIRPORT2), use_container_width=True)

    @st.cache(allow_output_mutation=True)
    def make_fig6(AIRPORT1,AIRPORT2):
        df_europe_ref = df.groupby(['YEAR','MONTH_MON','DATE']).sum()['FLT_ASMA_UNIMP_2'].reset_index()
        df_europe_ref['APT_NAME'] = 'Europe (Reference)'
        df_europe_ref.sort_values('DATE',inplace=True)
        df_tmp = pd.concat([df,df_europe_ref])

        df_tmp = df_tmp[df_tmp['APT_NAME'].isin([AIRPORT1, AIRPORT2])]
        df_tmp = change_column_names(df_tmp)
        fig = px.line(df_tmp, x='Month', y='IFR flights with unimpeded reference time', title='IFR flights with unimpeded reference time over time comparison',color='Year',line_dash='Airport name')
        return fig
    col8.plotly_chart(make_fig6(AIRPORT1,AIRPORT2), use_container_width=True)
    st.markdown('##### Comparative annual ASMA time flight statistics')
    col9, col10 = st.columns(2)

    @st.cache(allow_output_mutation=True)
    def make_fig7(AIRPORT):
        df_eu_reference = df.groupby('YEAR').mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_eu_reference.sort_values('YEAR',inplace=True)
        df_eu_reference['APT_NAME'] = 'Europe (Reference)'
        df_tmp = df.groupby(['APT_NAME','YEAR']).mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_tmp = pd.concat([df_tmp,df_eu_reference])
        df_tmp = df_tmp[df_tmp['APT_NAME'].isin([AIRPORT])]

        df_tmp = change_column_names(df_tmp)

        fig = px.bar(df_tmp, x='Year', y=['Avg. unimpeded ASMA time','Avg. additional ASMA time'], title='Average ASMA Time for ' + AIRPORT  )
        fig.layout.yaxis=dict(title='Avg. ASMA Time (minutes)')
        return fig

    col9.plotly_chart(make_fig7(AIRPORT1), use_container_width=True)
    col10.plotly_chart(make_fig7(AIRPORT2), use_container_width=True)

    st.markdown('##### Comparative monthly ASMA time flight statistics')
    col11_, col12_ = st.columns(2)
    col11_.markdown('This section allows to view more granular data on the monthly level. Please select the year of interest.')
    YEAR = col12_.selectbox('Year of Interest', df['YEAR'].unique())
    col11, col12 = st.columns(2)
    @st.cache(allow_output_mutation=True)
    def make_fig8(AIRPORT,YEAR):
        df_tmp = df[df['YEAR'] == YEAR]
        df_eu_reference = df_tmp.groupby(['MONTH_MON','MONTH_NUM']).mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_eu_reference = df_eu_reference.sort_values('MONTH_NUM')
        df_eu_reference['APT_NAME'] = 'Europe (Reference)'

        df_tmp = df_tmp.groupby(['APT_NAME','MONTH_MON','MONTH_NUM']).mean()[['AVG_UNIMPEDED_ASMA_TIME','AVG_ADDITIONAL_ASMA_TIME']].reset_index()
        df_tmp = df_tmp.sort_values('MONTH_NUM')

        df_tmp = pd.concat([df_tmp,df_eu_reference])
        df_tmp = df_tmp[df_tmp['APT_NAME']==AIRPORT]

        df_tmp = change_column_names(df_tmp)

        fig = px.bar(df_tmp, x='Month', y=['Avg. unimpeded ASMA time','Avg. additional ASMA time'], title='Average ASMA Time for ' + AIRPORT +' in ' + str(YEAR))
        fig.layout.yaxis=dict(title='Avg. ASMA Time (minutes)')
        return fig
    
    col11.plotly_chart(make_fig8(AIRPORT1,YEAR), use_container_width=True)
    col12.plotly_chart(make_fig8(AIRPORT2,YEAR), use_container_width=True)

    st.markdown('#### European total IRF flight statistics and 2022 projection using [Prophet](https://facebook.github.io/prophet/)')
    col13,col14 = st.columns(2)
    
    col13.image('resources/fb_prophet_prediction.png')
    with col14.expander('Additional information about Prophet'):
        st.markdown("""
        #### [Prophet](https://facebook.github.io/prophet/)
        Prophet (developed by Meta) is an open-source algorithm for generating time-series models that uses a few old ideas with some new twists. It is particularly good at modeling time series that have multiple seasonalities and doesn’t face some of the drawbacks of other algorithms. At its core is the sum of three functions of time plus an error term: growth g(t), seasonality s(t), holidays h(t) , and error e :

        * The growth function models the overall trend of the data. The old idea should be familiar to anyone with a basic knowledge of linear and logistic functions. The new idea incorporated into Facebook prophet is that the growth trend can be present at all points in the data or can be altered at what Prophet calls “changepoints”.
        * The seasonality function is simply a Fourier Series as a function of time. If you are unfamiliar with Fourier Series, an easy way to think about it is the sum of many successive sines and cosines. Each sine and cosine term is multiplied by some coefficient. This sum can approximate nearly any curve or in the case of Facebook Prophet, the seasonality (cyclical pattern) in our data. 
        * The holiday function allows Facebook Prophet to adjust forecasting when a holiday or major event may change the forecast. It takes a list of dates (there are built-in dates of US holidays or you can define your own dates) and when each date is present in the forecast adds or subtracts value from the forecast from the growth and seasonality terms based on historical data on the identified holiday dates.
        """)
    with col14.expander('Additional information and interpretation'):
        st.markdown("""
        #### Additional information
        The graph left provides the following information:
        * x-axis: The date
        * y-axis: The total number of inbound IFR flights in Europe
        * The black dots: Actual datapoints indicating the total number of inbound IFR flights in Europe
        * The blue line: Fitted function based on the available data
        * Shaded blue area: Uncertainty of the fitted function

        You can see the data ends before 2022. The fitted function predicts the IFR flight statistics for 2022. 
        
        #### Interpretation
        According to the timeseries projection it is expected that flight numbers will likely normalize to pre-covid numbers within 2022.""")

