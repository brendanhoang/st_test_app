from security import get_security, chart_security, calc_std_vol, chart_security_plotly
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas_ta as ta

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
        st.session_state['df'] = data
        sec = yf.Ticker(ticker) # INCORP YF TICKER CLASS
        st.header(f'{sec.info['shortName']} ({ticker})')
    except:
        st.error(f'Unable to find stock {ticker}. Please try again with valid ticker.')
        st.stop()

    with st.sidebar:
        with st.expander('See dataframe with all time series columns:',expanded=True):
            de = st.data_editor(data,
                    column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                    'close':st.column_config.NumberColumn('Closing Price',format="$ %.2f")},
                                    disabled=True)


if st.session_state.stock:
    col1, col2, col3 = st.columns(3)

    last_px = data.iloc[-1]['close']
    volume = sec.info['volume']
    try:
        b = sec.info['beta']
    except:
        b = sec.info['beta3Year']

    with st.container(border=True):
        col1.metric(label="Current Price:", value=f'${last_px:.2f}')
    with st.container(border=True):
        col2.metric("Beta:", value = b, help = '5Y Monthly')
    with st.container(border=True):
        col3.metric("Volume:", value = f'{volume:,}', help='average volume')

    options = st.multiselect(
        "Select desired indicators to graph", 
        ["sma200","ema20","ema50"],
        ["sma200","ema20","ema50"],
        placeholder = 'Currently nothing selected - click here to add indicator(s) to the plot.',
        help = "'sma200' is the 200 day simple moving average. 'ema' is exponential moving average for 20/50 days"
    )

    df = data.loc[:,options]
    df.insert(0,"close price",data['close'])
    st.session_state.returns = df # stored is only the selected columns from ema20,ema50,sma200

    tab1,tab2 = st.tabs(["Plotly chart style (new)","Matplotlib chart style (old)"])

    # *** MUST PASS IN DF DIRECTLY HERE TO CHART FUNCTION OR ELSE IT WONT UPDATE *** 
    with tab1:
        st.plotly_chart(chart_security_plotly(df,t=ticker),on_select='rerun') 
    with tab2:
        st.pyplot(chart_security(df,t=ticker))


    d = data.copy()
    hv = calc_std_vol(d,window=30)
    hv.rename("hvol",inplace=True)

    vdf = hv.to_frame()
    vdf['log_returns'] = (d["close"] / d["close"].shift(1)).apply(np.log)
    rsi = ta.rsi(data['close'])
    vdf['rsi']=rsi
    
    with st.sidebar:
        with st.expander('See dataframe with H vol, log returns, and RSI:'):
            edf=st.data_editor(vdf,
                    column_config={'Date':st.column_config.DateColumn(format="YYYY-MM-DD"),
                                                                            })
                                                                                
    v = hv.iloc[-1]

    cm1,cm2,_ = st.columns([.5,.7,4])
    with cm1.container(border=True):
        st.metric('30 day historical volatility:',value=f'{v:.4f}')
    with cm2.container(border=True):
        st.metric('Relative Strength Index (RSI):',value=f'{rsi.iloc[-1]:.4f}',help='calculated with closing prices from last 14 days.')

    if st.checkbox('click to show graph of historical 30 day volatility',value=False):
        out = st.line_chart(hv)
        
    st.markdown(f'<span style="font-size: 14px">**Source:** Yahoo Finance API | **Date:** {datetime.date.today().strftime("%m.%d.%Y")} | **Author:** Brendan Hoang </span>', unsafe_allow_html=True)


# def get_signals(data):
#     in_long = False
#     trade_log = []
#     for idx,row in data.iterrows():
#         if (row['ema20'] > row['ema50']) and (not in_long):
#             in_long = True
#             trade_log.append({
#                 'date':idx,
#                 'Action':'B',
#                 'price':row['close']
#             }
#             )
#         elif (row['ema20'] < row['ema50']) and (in_long):
#             in_long = False
#             trade_log.append({
#                 'date': idx,
#                 'Action':'S',
#                 'price':row['close']
#             }
#             )
#     return trade_log

# tl=get_signals(st.session_state['df'])
# trades = pd.DataFrame(tl)


# st.session_state.df

# fig=px.line(st.session_state.df,title='PLOTLY LINE CHART')
# fig.update_xaxes(
#     dtick="M1",
#     tickformat="%b\n%Y")
# st.plotly_chart(fig,theme=None)