import streamlit as st
import yfinance as yf

# st.set_page_config(page_title="More Info", page_icon="📈")

# @st.cache_data
st.title('Additional Information')
t = st.session_state.stock
sec = yf.Ticker(t)
st.subheader(f'{t.upper()}')

t1,t2,t3 = st.tabs(['Company Description','News','Analyst Recommendations'])

with t1:
    st.write(sec.info['longBusinessSummary'])
with t2:
    st.write(sec.news)
with t3:
    st.table(sec.recommendations_summary)
