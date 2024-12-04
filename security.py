import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

oneyr = datetime.datetime.now() - datetime.timedelta(days=1*365)
start_date = oneyr.strftime("%Y-%m-%d")


def get_security(ticker):
    df = _pull_security_data(ticker)
    return df


def _calc_ma(df,n):
    '''
    Arguments: 
    df = security df from get_security()
    n = window / number of days
    Returns: 200 day sma?
    '''
    out = df.copy()
    out.columns = ['close']
    out['sma200'] = out['close'].rolling(n).mean()
    out['ema20'] = out['close'].ewm(span=20).mean()
    out['ema50'] = out['close'].ewm(span=50).mean()
    return out

def _pull_security_data(ticker):
    '''
    Arguments: ticker (string)
    Returns: time series of px data from last year (dataframe)
    '''
    data = yf.download(ticker,start='2010-01-01')['Adj Close']
    data = _calc_ma(data,200)
    return data[start_date:]


# plt.plot(df.index,df.iloc[:,:1],label='close')
# plt.plot(df.index,df.iloc[:,:1],label='close')


def chart_security(df,t):
    # y=['Closing Price','Simple Moving Avg 200 days']
    plt.figure()
    df.plot(style={'sma200':'--', 'ema20':':', 'ema50':':'}, figsize=(12,8), x_compat=True)
    plt.ylabel('Price in USD')
    plt.xlabel('')
    plt.title(f'1 Year Price Chart for {t}')

    # # setting customized ticklabels for x axis 
    # pos = [ '1959-01-01', '1959-02-01', '1959-03-01', '1959-04-01',  
    #    '1959-05-01', '1959-06-01', '1959-07-01', '1959-08-01', 
    #    '1959-09-01', '1959-10-01', '1959-11-01', '1959-12-01'] 
  
    # lab = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',  
    #    'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'] 
    # plt.xticks( pos, lab) 
    # ax.set_xticks(df.index)
    plt.legend()
    plt.show()
    return plt




















