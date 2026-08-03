import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="NSE Live Market Insights")
st.title("📊 Live Market Insights Dashboard (NSE)")

# 1. STOCKS WATCHLIST (તમારી CSV ફાઈલ મુજબ)
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

# 2. SECTOR WATCHLIST (તમારી CSV ફાઈલ મુજબ)
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

# Pivot Points Calculation (R1 & S1)
def calculate_pivot_points(df):
    high = df['High'].iloc[-2]
    low = df['Low'].iloc[-2]
    close = df['Close'].iloc[-2]
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    return r1, s1

@st.cache_data(ttl=60)
def scan_stocks():
    bullish_list, bearish_list = [], []
    all_stocks = []
    
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
            
            r1, s1 = calculate_pivot_points(df)
            symbol_name = ticker.replace('.NS', '')
            
            all_stocks.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
            
            # Chartink Strict Rules
            if (ltp > prev_15m_high) and (ltp > prev_25_high) and (ltp > r1) and (pct_change > 1.0):
                bullish_list.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
            elif (ltp < prev_15m_low) and (ltp < prev_25_low) and (ltp < s1) and (pct_change < -1.0):
                bearish_list.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
        except: pass
        
    df_bull = pd.DataFrame(bullish_list)
    df_bear = pd.DataFrame(bearish_list)
    df_all = pd.DataFrame(all_stocks)

    # Fallback: જો શરતોવાળો કડક ડેટા ન મળે તો % Change મુજબ ટોપ ડેટા બતાવો
    if df_bull.empty and not df_all.empty:
        df_bull = df_all[df_all['Change %'] > 0].sort_values(by='Change %', ascending=False)
    if df_bear.empty and not df_all.empty:
        df_bear = df_all[df_all['Change %'] < 0].sort_values(by='Change %', ascending=True)

    return df_bull, df_bear

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

# Fetch Data
bull_stock, bear_stock = scan_stocks()
bull_sec, bear_sec = scan_sectors()

# UI Layout (4 Widgets)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 1. BULLISH STOCKS")
    st.dataframe(bull_stock.sort_values(by='Change %', ascending=False), use_container_width=True) if not bull_stock.empty else st.info("કોઈ સ્ટોક મળ્યો નથી")

    st.subheader("📈 3. BULLISH SECTORS")
    st.dataframe(bull_sec.sort_values(by='Change %', ascending=False), use_container_width=True) if not bull_sec.empty else st.info("કોઈ સેક્ટર મળ્યું નથી")

with col2:
    st.subheader("🔴 2. BEARISH STOCKS")
    st.dataframe(bear_stock.sort_values(by='Change %', ascending=True), use_container_width=True) if not bear_stock.empty else st.info("કોઈ સ્ટોક મળ્યો નથી")

    st.subheader("📉 4. BEARISH SECTORS")
    st.dataframe(bear_sec.sort_values(by='Change %', ascending=True), use_container_width=True) if not bear_sec.empty else st.info("કોઈ સેક્ટર મળ્યું નથી")
            
