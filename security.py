import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math
import plotly.express as px

oneyr = datetime.datetime.now() - datetime.timedelta(days=1*365)
start_date = oneyr.strftime("%Y-%m-%d")


def get_security(ticker):
    try:
        df = _pull_security_data(ticker)
        df.isnull().values.any()
        df = df.dropna()
    except:
        st.warning('Unable to find stock. Please check spelling')
    return df


def _calc_ma(df,n):
    '''
    Arguments: 
    df = security df from get_security()
    n = window / number of days
    Returns: 200 day sma?
    '''
    out = df.rename(columns={'Adj Close':'close'}).copy()
    # out.columns = ['close']
    out['sma200'] = out['close'].rolling(n).mean()
    out['ema20'] = out['close'].ewm(span=20).mean()
    out['ema50'] = out['close'].ewm(span=50).mean()
    return out

@st.cache_data
def _pull_security_data(ticker):
    '''
    Arguments: ticker (string)
    Returns: time series of px data from last year (dataframe)
    '''
    data = yf.download(ticker,start='2010-01-01')['Adj Close']
    data = _calc_ma(data,200)
    return data[start_date:]



# NEED TO DEBUG THIS - TOO MANY COLS
def pull_security_data(ticker,s,e,ohlv_cols=False):
    if ohlv_cols:
        data = yf.download(ticker,start=s,end=e)
    else:
        data = yf.download(ticker,start=s,end=e)['Adj Close']

    new_data = _calc_ma(data,200)

    new_data.isnull().values.any()
    new_data = new_data.dropna()
    return new_data


def chart_security(df,t):
    # y=['Closing Price','Simple Moving Avg 200 days']
    plt.figure()
    df.plot(style={'sma200':'--', 'ema20':':', 'ema50':':'}, figsize=(12,7), x_compat=True)
    plt.ylabel('Price in USD')
    plt.xlabel('')
    plt.title(f'1 Year Price Chart for {t}')
    plt.legend()
    plt.show()
    return plt

def chart_security_plotly(df,t):
    fig=px.line(df, 
                title=f'1 YR PLOTLY LINE CHART FOR {t}', 
                color_discrete_map={
                    'close price':'cyan',
                    'sma200': 'orange',
                    'ema20': 'magenta',
                    'ema50': 'red'
                },
                line_dash_map={'sma200':'dash',
                               'ema20':'dash'})
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig.update_layout(
        xaxis_title = 'Date',
        yaxis_title = 'Price in USD',
        legend_title_text = "",
        # legend = dict(yanchor="top",
        #                 y=0.99,
        #                 xanchor="left",
        #                 x=0.01)
    )
    # fig.add_trace(go.Scatter())
    return fig

def calc_std_vol(price_data, window, trading_periods=252, clean=False):
    log_return = (price_data["close"] / price_data["close"].shift(1)).apply(np.log)
    result = log_return.rolling(window=window, center=False).std() * math.sqrt(trading_periods)

    if clean:
        return result.dropna()
    else:
        return result

















