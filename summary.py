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


st.title('Summary Metrics')
st.info(f'Last run: {datetime.datetime.today().strftime("%H:%M - %m/%d/%Y")}')

if not st.session_state.stock:
    st.warning('Please enter the name of a stock in left sidebar to begin.')

if st.session_state.stock:
    ticker = st.session_state.stock.upper()
    
    try:
        data = get_security(ticker) # dataframe dtype currrently
        sec = yf.Ticker(ticker) # INCORP YF TICKER CLASS
        st.header(f'{sec.info['shortName']} ({ticker})')
    except:
        st.error(f'Unable to find stock {ticker}. Please try again with valid ticker.')
        st.stop()

    with st.sidebar:
        with st.expander('Show dataframe:'):
            de = st.data_editor(data,
                    column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                    'close':st.column_config.NumberColumn('Closing Price',format="$ %.2f")})


if st.session_state.stock:
    col1, col2, col3 = st.columns(3)
    px = data.iloc[-1]['close']
    volume = sec.info['volume']
    with st.container(border=True):
        col1.metric(label="Current Price:", value=f'${px:.2f}')
    with st.container(border=True):
        col2.metric("Beta:", value = sec.info['beta'], help = '5Y Monthly')
    with st.container(border=True):
        col3.metric("Volume:", value = f'{volume:,}', help='average volume')

    options = st.multiselect(
        "Select indicators", 
        ["sma200","ema20","ema50"],
        ["sma200","ema20","ema50"],
        help = "'sma200' is the 200 day simple moving average. 'ema' is exponential moving average for 20/50 days"
    )

    df = data.loc[:,options]
    df.insert(0,"close price",data['close'])
    st.pyplot(chart_security(df,t=ticker))

    d = data.copy()
    hv = calc_std_vol(d,window=30)
    hv.rename("hvol",inplace=True)

    vdf = hv.to_frame()
    vdf['log_returns'] = (d["close"] / d["close"].shift(1)).apply(np.log)

    st.sidebar.caption('Dataframe used to calculate historical volatility:')
    st.sidebar.data_editor(vdf,
                    column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                                                            }
                                                                            )
    
    v = hv.iloc[-1]
    st.metric('30 day historical volatility:',value=f'{v:.4f}')
    st.line_chart(hv)
    st.markdown(f'<span style="font-size: 14px">**Source:** Yahoo Finance API | **Date:** {datetime.date.today().strftime("%m.%d.%Y")} | **Author:** Brendan Hoang </span>', unsafe_allow_html=True)





