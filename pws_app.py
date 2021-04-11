import pandas as pd
import numpy as np
import requests
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from datetime import date, timedelta, datetime
import plotly.express as px

# ===========|============FUNCTIONS===========|============


def plot_temp(df):
    '''
    '''
    fig = px.line(df,
                  x='Timestamp_Local',
                  y=['Temp_Avg', 'DewPt_Avg'],
                  labels={'Temp_Avg': 'Temperature', 'DewPt_Avg': 'Dewpoint'},
                  width=1200,
                  height=500,
                  color_discrete_map={'Temp_Avg': 'red', 'DewPt_Avg': 'green'},
                  template='plotly_dark'
                  )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x",
                      xaxis={'title': 'Timestamp', 'showgrid': False},
                      yaxis={'title': 'Temperature(F)'},
                      title_x=0.5,
                      title={'font': {'size': 20}, 'text': 'Temperature and Dewpoint'},
                      showlegend=False
                      )
    fig['data'][0]['name'] = 'Temperature'
    fig['data'][1]['name'] = 'Dewpoint'

    ph_tempplot.plotly_chart(fig)


def plot_wind(df):
    '''
    '''
    fig = px.line(df,
                  x='Timestamp_Local',
                  y=['WindSpeed_High', 'WindGust_High'],
                  labels={'WindSpeed_High': 'Wind Speed', 'WindGust_High': 'Gust'},
                  width=1200,
                  height=500,
                  color_discrete_map={'WindSpeed_High': 'blue', 'WindGust_High': 'lightblue'},
                  template='plotly_dark'
                  )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x",
                      xaxis={'title': 'Timestamp', 'showgrid': False},
                      yaxis={'title': 'Speed(mph)'},
                      title_x=0.5,
                      title={'font': {'size': 20}, 'text': 'Average Wind Speed and Gusts'},
                      showlegend=False
                      )
    fig['data'][0]['name'] = 'Wind Speed'
    fig['data'][1]['name'] = 'Gust'

    ph_windplot.plotly_chart(fig)


def refresh_page():
    '''
    '''

def call_api(url):
    '''
    '''
    resp_curr = requests.get(url)
    resp_curr_json = resp_curr.json()
    st.subheader('')
    df = pd.json_normalize(resp_curr_json, 'observations')
    df.columns = column_names

    return df


# Set variables
today = date.today()
api_key = '4037e029ae6a43dcb7e029ae6a23dc8e'
column_names = ['Station_ID', 'Timezone', 'Timestamp_UTC', 'Timestamp_Local', 'epoch', 'Lat', 'Lon', 'solarRadiationHigh', 'uvHigh', 'WindDir_Avg', 'Humidity_High', 'Humidity_Low', 'Humidity_Avg', 'qcStatus', 'Temp_High', 'Temp_Low', 'Temp_Avg', 'WindSpeed_High', 'WindSpeed_Low', 'WindSpeed_Avg', 'WindGust_High', 'WindGust_Low', 'WindGust_Avg', 'DewPt_High', 'DewPt_Low', 'DewPt_Avg', 'WindChill_High', 'WindChill_Low', 'WindChill_Avg', 'HeatIndex_High', 'HeatIndex_Low', 'HeatIndex_Avg', 'Pressure_Max', 'Pressure_Min', 'PressureTrend', 'PrecipRate', 'PrecipTotal']

# Construct app view
st.set_page_config(layout='wide', page_title='PWS Observations', page_icon='https://p1.hiclipart.com/preview/994/283/642/rainmeter-tabbed-dock-grey-and-yellow-lightning-icon-png-clipart.jpg')

# Background color
st.markdown("""
<style>
body {
    color: #000;
    background-color: #A0A0A0;
}
</style>
    """, unsafe_allow_html=True)

# Sidebar background
st.markdown(
    """
<style>
.css-1aumxhk {
background-color: #B4B2B2;
background-image: none;
color: #000000
}
</style>
""",
    unsafe_allow_html=True,
)

cola, colb, colc = st.beta_columns([1,4,1])
colb.title("-Hammer Lane Weather Observation-")
today_date = today.strftime("%Y%m%d")


# Show current observation table and plot in body
col1, col2, col3 = st.beta_columns([.5,6,1])
url = f'https://api.weather.com/v2/pws/observations/all/1day?stationId=KCAARCAT31&format=json&units=e&numericPrecision=decimal&apiKey={api_key}'
df_curr = call_api(url)

# Button to refresh current obs
col1.button('Refresh')

# Current obs table
col2.markdown(f'''Current Observation | Temperature  | Feels Like | Dewpoint | Humidity | Wind Speed | Wind Gusts | Pressure | Daily Rain |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
{df_curr.Timestamp_Local[len(df_curr)-1]} | {df_curr.Temp_Avg[len(df_curr)-1]} F  | {df_curr.HeatIndex_Avg[len(df_curr)-1]} F  | {df_curr.DewPt_Avg[len(df_curr)-1]} F | {df_curr.Humidity_Avg[len(df_curr)-1]}% | {df_curr.WindSpeed_Avg[len(df_curr)-1]} mph | {df_curr.WindGust_High[len(df_curr)-1]} mph | {df_curr.Pressure_Max[len(df_curr)-1]} mb | {df_curr.PrecipTotal[len(df_curr)-1]} in |''')

ph_tempplot = st.empty()
ph_windplot = st.empty()

# Plot current conditions by default
plot_temp(df_curr)
plot_wind(df_curr)


st.sidebar.markdown('# Plot Historical Data')
if st.sidebar.checkbox('Single Date', False):
    date = st.sidebar.text_input("Enter Date(YYYYMMDD)", (datetime.now() - timedelta(1)).strftime('%Y%m%d'))
    url = f'https://api.weather.com/v2/pws/history/hourly?stationId=KCAARCAT31&format=json&units=e&numericPrecision=decimal&date={date}&apiKey={api_key}'
    df_hist = call_api(url)
    # Plots
    plot_temp(df_hist)
    plot_wind(df_hist)
# if st.sidebar.checkbox('Date Range'):
#     min_value = datetime.strptime('20191001', '%Y%m%d')
#     max_value = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
#     start_time = st.sidebar.slider("When do you start?",
#                            value=datetime,
#                            format="YYYYMMDD",
#                            min_value=min_value,
#                            max_value=max_value,
#                            step=1)
