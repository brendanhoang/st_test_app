import security
from security import get_security, chart_security

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


oneyr = datetime.datetime.now() - datetime.timedelta(days=1*365)
start_date = oneyr.strftime("%Y-%m-%d")

st.title('Security Data')

t = st.text_input('Enter stock ticker:',value='NVDA',placeholder = 'SBUX, AAPL, etc.', help='Enter name of ticker (not case sensitive)')
ticker = t.upper()

# e = NameError("Please enter a valid stock ticker and hit enter.")
# err_info = st.info("Please enter a valid stock ticker and hit enter.")
if ticker:
    data = get_security(ticker)
else:
    st.info("Please enter a valid stock ticker before pressing enter enter.")
# st.write(data.index)


# r = data.pct_change().dropna()
# cum_r = (r+1).cumprod()

px = data.iloc[-1]['close']

st.metric(label="Current Price:", value=f'${px:.2f}')

# df = data.assign(avg_return=cum_r,sma200=sma200).rename(columns={tickers:'close'})


# col1, col2 = st.columns(2)
# with col1:
# 	st.metric(label="Current Price:", value=f'{px:.2f}')

with st.sidebar:
    with st.expander('Click to view base data:'):
        st.dataframe(data.tail(30))



options = st.multiselect(
    "Select indicators", 
    ["sma200","ema20","ema50"],
    ["sma200","ema20","ema50"]
)

df = data.loc[:,options]
df.insert(0,"close price",data['close'])

st.pyplot(chart_security(df,t=ticker))

dt = datetime.date.today().strftime("%m.%d.%Y")
st.markdown(f'<span style="font-size: 14px">**Source:** Yahoo Finance API | **Date:** {dt} | **Author:** Brendan Hoang </span>', unsafe_allow_html=True)

















