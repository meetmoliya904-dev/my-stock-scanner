import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="Live Market Insights")
st.title("📊 Live Market Insights Dashboard (NSE)")

# 1. Stocks Watchlist (તમારી CSV ફાઈલ મુજબના તમામ શેરો)
STOCKS = [
    'AUBANK.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 
    'ALKEM.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'AUROPHARMA.NS', 
    'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BALKRISIND.NS', 'BANDHANBNK.NS', 
    'BANKBARODA.NS', 'BERGEPAINT.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 
    'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CANBK.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 
    'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 
    'DABUR.NS', 'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 
    'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 
    'HAVELLS.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HAL.NS', 
    'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDFCFIRSTB.NS', 'INDIAMART.NS', 
    'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'IOC.NS', 'IRCTC.NS', 'ITC.NS', 
    'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'LTIM.NS', 'LT.NS', 
    'LUPIN.NS', 'M&M.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 
    'MRF.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 
    'PAGEIND.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 
    'POLYCAB.NS', 'POWERGRID.NS', 'REC.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBILIFE.NS', 'SBIN.NS', 
    'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SUNPHARMA.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 
    'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 
    'TVSMOTOR.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS'
]

# 2. Sector Watchlist (તમારી CSV ફાઈલ મુજબના સેક્ટર્સ)
SECTORS = {
    'Nifty Bank': '^NSEBANK', 
    'Nifty IT': '^CNXIT', 
    'Nifty Pharma': '^CNXPHARMA', 
    'Nifty Financial Services': 'NIFTY_FIN_SERVICE.NS',
    'Nifty FMCG': '^CNXFMCG',
    'Nifty Metal': '^CNXMETAL',
    'Nifty PSU Bank': '^CNXPSU'
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
            
            # Bullish Condition
            if (ltp > prev_15m_high) and (ltp > prev_25_high) and (pct_change > 1.0):
                bullish_list.append({'Stock': symbol_name, 'LTP': round(ltp, 2), 'Change %': pct_change})
            # Bearish Condition
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

# Fetch Data
bull_stock, bear_stock = scan_stocks()
bull_sec, bear_sec = scan_sectors()

# UI Layout (4 Widgets)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 1. BULLISH STOCKS")
    if not bull_stock.empty:
        st.dataframe(bull_stock.sort_values(by='Change %', ascending=False), use_container_width=True)
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
        st.dataframe(bear_stock.sort_values(by='Change %', ascending=True), use_container_width=True)
    else:
        st.info("કોઈ Bearish સ્ટોક મળ્યો નથી")

    st.subheader("📉 4. BEARISH SECTORS")
    if not bear_sec.empty:
        st.dataframe(bear_sec.sort_values(by='Change %', ascending=True), use_container_width=True)
    else:
        st.info("કોઈ Bearish સેક્ટર મળ્યું નથી")
                  
