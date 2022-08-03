import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
import streamlit as st

st.set_page_config(layout="wide")


SRC_PATH = os.environ.get('SRC_PATH')  #  path to source code os.path.abspath('.')
DB_NAME = os.environ.get('DB_NAME')  #  [database will be one directory above source code]
IEX_KEY = os.environ.get('IEX_KEY')  # IEX api key to get market data

# Create engine
engine = sqlalchemy.create_engine(f"sqlite:///{SRC_PATH.replace('/MarketView', '')}/{DB_NAME}")


last_feed = sorted([table for table in engine.table_names() if 'last' in table], reverse=True)
quote_feed = sorted([table for table in engine.table_names() if 'quote' in table], reverse=True)


clean_df = \
(
    pd.read_sql(last_feed[0], engine, index_col='symbol').merge(
        pd.read_sql(quote_feed[0], engine, index_col='symbol'),
        on='symbol'
    )
    
    # prepare dataframe
    .assign(
        prev_close = lambda df: df['price'],
        last = lambda df: df['lastSalePrice'],
    )
    
    .drop(columns=[
            'price',
            'bidSize',
            'askSize',
            'size',
            'time',
            'sector',
            'securityType',
            'lastUpdated',
            'lastSalePrice',
            'lastSaleSize',
            'lastSaleTime',
            'volume',
            ]
        )
    
    
    [
        lambda df:
        (df['bidPrice'] > 0)
        & (df['askPrice'] > 0)
        & (df['last'] > 0)
    ]
    
    
    .assign(
            spd_pct = lambda df: (df['askPrice'] / df['bidPrice'] - 1) * 100,
            pct_chg = lambda df: (df['last'] / df['prev_close'] - 1) * 100,
        )
    
        
)




liquidity_filter_value = st.slider("Filter for Liquidity", min_value=0, max_value=(len(clean_df)//2), value=(len(clean_df)//2), step=25)
liquid_df = clean_df.sort_values(by='spd_pct')

fig = plt.figure(figsize=(12,5))
plt.plot(liquid_df.spd_pct.values[:4000], label='Universe')
plt.plot(liquid_df.iloc[:liquidity_filter_value].spd_pct.values, label='Liquid Securities')
plt.legend()


st.write(f"""
Number of securities: {liquidity_filter_value} | 
Max Spread: {liquid_df.iloc[:liquidity_filter_value].spd_pct.max()} | 
""")

st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.write("Top Gainers")
    st.dataframe(
        liquid_df.iloc[:liquidity_filter_value].sort_values(by='pct_chg', ascending=False)[['last', 'pct_chg']].head(15)
    )

with col2:
    st.write("Top Losers")
    st.dataframe(
        liquid_df.iloc[:liquidity_filter_value].sort_values(by='pct_chg', ascending=True)[['last', 'pct_chg']].head(15)
    )


