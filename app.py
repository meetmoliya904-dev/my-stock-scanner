import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="NSE Live Market Insights")
st.title("📊 Live Market Insights Dashboard (NSE)")

# 1. STOCKS WATCHLIST
STOCKS = [
    'AUBANK.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 
    'ALKEM.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'AUROPHARMA.NS', 
    'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BALKRISIND.NS', 'BANKBARODA.NS', 
    'BEL.NS', 'BHARATFORG.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BRITANNIA.NS', 
    'CANBK.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CUMMINSIND.NS', 'DABUR.NS', 
    'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ETERNAL.NS', 'GAIL.NS', 'GLENMARK.NS', 
    'GODREJCP.NS', 'GRASIM.NS', 'HDFCLIFE.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 
    'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'IDFCFIRSTB.NS', 'ICICIBANK.NS', 'IOC.NS', 
    'IGL.NS', 'INDUSTOWER.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IPCALAB.NS', 'ITC.NS', 'JINDALSTEL.NS', 
    'JIOFIN.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS', 'LT.NS', 'LUPIN.NS', 'MGL.NS', 'M&M.NS', 
    'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'NESTLEIND.NS', 'NMDC.NS', 
    'NTPC.NS', 'ONGC.NS', 'OIL.NS', 'PERSISTENT.NS', 'POWERGRID.NS', 'PNB.NS', 'RELIANCE.NS', 
    'SBILIFE.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SBIN.NS', 'SAIL.NS', 'SUNPHARMA.NS', 
    'SUNTV.NS', 'TATACONSUM.NS', 'TCS.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 
    'TECHM.NS', 'FEDERALBNK.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 
    'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UNITDSPR.NS', 'VEDL.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS'
]

# 2. SECTOR WATCHLIST
SECTORS = {
    'Bank Nifty': '^NSEBANK', 
    'Nifty IT': '^CNXIT', 
    'Nifty Pharma': '^CNXPHARMA', 
    'Nifty Fin Service': 'NIFTY_FIN_SERVICE.NS',
    'Nifty FMCG': '^CNXFMCG',
    'Nifty Metal': '^CNXMETAL',
    'Nifty PSU Bank': '^CNXPSU',
    'Nifty Realty': '^CNXREALTY'
}

@st.cache_data(ttl=60)
def scan_stocks():
    all_stocks = []
    for ticker in STOCKS:
        try:
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            if len(df) < 2: continue
            
            # Close Price & Daily Change calculation
            ltp = float(df['Close'].iloc[-1])
            prev_close = float(df['Close'].iloc[0])
            pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)
            symbol_name = ticker.replace('.NS', '')
            
            all_stocks.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
        except: pass
        
    df_all = pd.DataFrame(all_stocks)
    if not df_all.empty:
        # Bullish: Top Change % (> 0) | Bearish: Lowest Change % (< 0)
        bullish_df = df_all[df_all['Change %'] >= 0].sort_values(by='Change %', ascending=False)
        bearish_df = df_all[df_all['Change %'] < 0].sort_values(by='Change %', ascending=True)
        return bullish_df, bearish_df
    return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=60)
def scan_sectors():
    bull_sec, bear_sec = [], []
    for sec_name, symbol in SECTORS.items():
        try:
            df = yf.download(symbol, period="5d", interval="1d", progress=False)
            if len(df) >= 2:
                ltp = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                pct = round(((ltp - prev) / prev) * 100, 2)
                if pct >= 0: 
                    bull_sec.append({'Sector': sec_name, 'Change %': pct})
                else: 
                    bear_sec.append({'Sector': sec_name, 'Change %': pct})
        except: pass
    return pd.DataFrame(bull_sec), pd.DataFrame(bear_sec)

# Fetch Data
bull_stock, bear_stock = scan_stocks()
bull_sec, bear_sec = scan_sectors()

# UI Layout (4 Widgets)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 1. BULLISH STOCKS")
    if not bull_stock.empty:
        st.dataframe(bull_stock, use_container_width=True)
    else:
        st.info("કોઈ Bullish સ્ટોક મળ્યો નથી")

    st.subheader("📈 3. BULLISH SECTORS")
    if not bull_sec.empty:
        st.dataframe(bull_sec.sort_values(by='Change %', ascending=False), use_container_width=True)
    else:
        st.info("કોઈ Bullish સેક્ટર મળ્યું નથી")

with col2:
    st.subheader("🔴 2. BEARISH STOCKS")
    if not bear_stock.empty:
        st.dataframe(bear_stock, use_container_width=True)
    else:
        st.info("કોઈ Bearish સ્ટોક મળ્યો નથી")

    st.subheader("📉 4. BEARISH SECTORS")
    if not bear_sec.empty:
        st.dataframe(bear_sec.sort_values(by='Change %', ascending=True), use_container_width=True)
    else:
        st.info("કોઈ Bearish સેક્ટર મળ્યું નથી")
