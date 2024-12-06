import streamlit as st

st.set_page_config(layout="wide")

pages = {
    "Stock Analysis Pages": [
        st.Page("summary.py", title="Home"),
        st.Page("1_stock_info.py", title="Research"),
    ],
    "Other Features": [
        st.Page("2_backtest.py", title="Backtest"),
        # st.Page("trial.py", title="Try it out"),
    ],
}


placeholder = st.sidebar.empty()

if 'stock' not in st.session_state:
    st.sidebar.title('Start Here')

st.sidebar.text_input("Input ticker here:",placeholder = '(eg. NVDA)', help='Enter one stock only (not case sensitive)',key='stock')
placeholder.title(f'Displaying data for: {st.session_state.stock.upper()}')


pg = st.navigation(pages)
pg.run()
