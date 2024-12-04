from security import get_security, chart_security, calc_std_vol

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math

oneyr = datetime.datetime.now() - datetime.timedelta(days=1*365)
start_date = oneyr.strftime("%Y-%m-%d")

# st.set_page_config(
#     page_title="Stock Analysis",
#     page_icon="👋",
# )

st.title('Stock Analysis')

t = st.text_input('Enter stock ticker:',value='NVDA',placeholder = 'SBUX, AAPL, etc.', help='Enter name of ticker (not case sensitive)')
ticker = t.upper()

if ticker:
    data = get_security(ticker) # dataframe dtype currrently
    sec = yf.Ticker(ticker) # INCORP YF TICKER CLASS
    st.header(f'{sec.info['shortName']}')
else:
    st.info("Please enter a valid stock ticker before pressing enter enter.")


with st.sidebar:
    # st.header(f'{sec.info['shortName']}')
    with st.expander('Show dataframe:'):
        de = st.data_editor(data,
                column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                'close':st.column_config.NumberColumn('Closing Price',format="$ %.2f")
                                
                                
                                })


# r = data.pct_change().dropna()
# cum_r = (r+1).cumprod()



col1, col2, col3 = st.columns(3)
px = data.iloc[-1]['close']
volume = sec.info['volume']

with st.container(border=True):
    col1.metric(label="Current Price:", value=f'${px:.2f}')
with st.container(border=True):
    col2.metric("Beta:", value = sec.info['beta'], help = '5Y Monthly')
with st.container(border=True):
    col3.metric("Volume:", value = f'{volume:,}', help='average volume')

# with st.container(border=True):
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         px = data.iloc[-1]['close']
#         st.metric(label="Current Price:", value=f'${px:.2f}')
#     with col2:
#         st.metric("Beta:", value = sec.info['beta'], help = '5Y Monthly')
#     with col3:
#         volume = sec.info['volume']
#         st.metric("Volume:", value = f'{volume:,}')


# with st.container(border=True):
options = st.multiselect(
    "Select indicators", 
    ["sma200","ema20","ema50"],
    ["sma200","ema20","ema50"]
)

df = data.loc[:,options]
df.insert(0,"close price",data['close'])
st.pyplot(chart_security(df,t=ticker))


# st.title('Page 1')
# def page_2():
    # st.title('Page 2')
# pg = st.navigation([st.Page("app.py"), st.Page(page_2)])
# pg.run()

d = data.copy()
hv = calc_std_vol(d,window=30)
hv.rename("hvol",inplace=True)


vdf = hv.to_frame()
vdf['log_returns'] = (d["close"] / d["close"].shift(1)).apply(np.log)
vdf['log_returns_2'] = vdf['log_returns'].copy()

with st.sidebar:
    st.caption('historical vol time series')
    # st.dataframe(vdf,width=200)
    
    st.data_editor(vdf,
                   column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                  'log_returns_2':st.column_config.LineChartColumn("Log Returns",
                                                                          width="medium",
                                                                          y_min=-0.2,
                                                                          y_max=0.2)})


v = hv.iloc[-1]
st.metric('30 day H vol is around:',value=f'{v:.4f}')
st.line_chart(hv)


dt = datetime.date.today().strftime("%m.%d.%Y")
st.markdown(f'<span style="font-size: 14px">**Source:** Yahoo Finance API | **Date:** {dt} | **Author:** Brendan Hoang </span>', unsafe_allow_html=True)





