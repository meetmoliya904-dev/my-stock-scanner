import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="Live Market Insights")
st.title("📊 Live Market Insights Dashboard (NSE)")

STOCKS = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'TATAMOTORS.NS', 'ICICIBANK.NS', 
          'SBIN.NS', 'HDFCBANK.NS', 'AXISBANK.NS', 'LT.NS', 'BHARTIARTL.NS']

SECTORS = {
    'Nifty Bank': '^NSEBANK', 
    'Nifty IT': '^CNXIT', 
    'Nifty Auto': '^CNXAUTO', 
    'Nifty Pharma': '^CNXPHARMA',
    'Nifty FMCG': '^CNXFMCG'
}

@st.cache_data(ttl=60)
def scan_stocks():
    bullish_list, bearish_list = [], []
    for ticker in STOCKS:
        try:
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            if len(df) < 26: continue
            
            ltp = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[0])
            pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)
            
            prev_15m_high = float(df['High'].iloc[-2])
            prev_15m_low = float(df['Low'].iloc[-2])
            prev_25_high = float(df['High'].iloc[-26])
            prev_25_low = float(df['Low'].iloc[-26])
            
            symbol_name = ticker.replace('.NS', '')
            
            if (ltp > prev_15m_high) and (ltp > prev_25_high) and (pct_change > 1.0):
                bullish_list.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
            elif (ltp < prev_15m_low) and (ltp < prev_25_low) and (pct_change < -1.0):
                bearish_list.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
        except: pass
    return pd.DataFrame(bullish_list), pd.DataFrame(bearish_list)

@st.cache_data(ttl=60)
def scan_sectors():
    bull_sec, bear_sec = [], []
    for sec_name, symbol in SECTORS.items():
        try:
            df = yf.download(symbol, period="2d", interval="1d", progress=False)
            if len(df) >= 2:
                ltp = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                pct = round(((ltp - prev) / prev) * 100, 2)
                if pct >= 0: bull_sec.append({'Sector': sec_name, 'Change %': pct})
                else: bear_sec.append({'Sector': sec_name, 'Change %': pct})
        except: pass
    return pd.DataFrame(bull_sec), pd.DataFrame(bear_sec)

bull_stock, bear_stock = scan_stocks()
bull_sec, bear_sec = scan_sectors()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 1. BULLISH STOCKS")
    if not bull_stock.empty:
        st.dataframe(bull_stock, use_container_width=True)
    else:
        st.info("કોઈ સ્ટોક મળ્યો નથી")

    st.subheader("📈 3. BULLISH SECTORS")
    if not bull_sec.empty:
        st.dataframe(bull_sec, use_container_width=True)
    else:
        st.info("કોઈ સેક્ટર મળ્યું નથી")

with col2:
    st.subheader("🔴 2. BEARISH STOCKS")
    if not bear_stock.empty:
        st.dataframe(bear_stock, use_container_width=True)
    else:
        st.info("કોઈ સ્ટોક મળ્યો નથી")

    st.subheader("📉 4. BEARISH SECTORS")
    if not bear_sec.empty:
        st.dataframe(bear_sec, use_container_width=True)
    else:
        st.info("કોઈ સેક્ટર મળ્યું નથી")
              
