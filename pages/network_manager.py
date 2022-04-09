import streamlit as st
import lorem
import pandas as pd
from millify import millify
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit as st
import pickle

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def app():
    st.markdown("<h1 style='text-align: left; color: black;'>Network Manager Dashboard</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    col1.markdown("""
    Welcome to the Network Manager Dashboard. 
    
    The aim of this dashboard is to provide monitoring over time for the various countries and airport authorities for a network manager. For more information about the underlying data and the developer of this platform, please check out the ABOUT page.
    """)
    df = pd.read_feather('resources/ASMA_Additional_Time.feather')
    col1.markdown("""The metrics on the right hand side are Europe wide. Note that the <t style="color:#149414"><b>green</b></t> and <t style="color:#FF0000"><b>red</b></t> colored metrics (see right) indicate <t style="color:#149414"><b>increases</b></t>  or <t style="color:#FF0000"><b>decreases</b></t> relative to same metric the previous year.""", unsafe_allow_html=True)
    col1.markdown("""<b>Note: As a network manager you might be interested in obtaining the raw data. You can download the raw data here:</b>""",unsafe_allow_html=True)
    df_xlsx = to_excel(df)
    col1.download_button(label='📥 Download Raw Data', data=df_xlsx, file_name= 'ASMA_Additional_Time.xlsx')
    
    FLT_2021 = df[df['YEAR']==2021]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2020 = df[df['YEAR']==2020]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2019 = df[df['YEAR']==2019]['FLT_ASMA_UNIMP_2'].sum()
    FLT_2018 = df[df['YEAR']==2018]['FLT_ASMA_UNIMP_2'].sum()

    col2.metric("Inbound IFR flights 2019", millify(FLT_2019), delta=round(((FLT_2019-FLT_2018)/FLT_2018)*100,2), delta_color="normal")
    col2.metric("Inbound IFR flights 2020", millify(FLT_2020), delta=round(((FLT_2020-FLT_2019)/FLT_2019)*100,2), delta_color="normal")
    col2.metric("Inbound IFR flights 2021", millify(FLT_2021), delta=round(((FLT_2021-FLT_2020)/FLT_2020)*100,2), delta_color="normal")

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

    st.markdown('## Geographical Overviews')
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

    