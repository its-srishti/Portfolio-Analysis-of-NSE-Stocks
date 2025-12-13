import streamlit as st, yfinance as yf, quantstats as qs, pandas as pd, plotly.express as px
import tempfile, os

## Sidebar Contents
st.set_page_config(page_title = "Portfolio Analytics Dashboard", layout="wide")
st.title("Portfolio Analytics Dashboard Using Quantstats")

st.sidebar.header("Portfolio Configuration")
nse_tickers = [
    "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS",
    "LT.NS", "KOTAKBANK.NS", "SBIN.NS", "HCLTECH.NS", "ITC.NS",
    "AXISBANK.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "WIPRO.NS",
    "POWERGRID.NS", "NTPC.NS", "TECHM.NS", "ONGC.NS", "JSWSTEEL.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "ADANIENT.NS", "ADANIPORTS.NS", "COALINDIA.NS",
    "BAJAJFINSV.NS", "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "INDUSINDBK.NS", "M&M.NS",
    "BAJAJ-AUTO.NS", "BRITANNIA.NS", "CIPLA.NS", "HDFCLIFE.NS", "SBILIFE.NS",
    "APOLLOHOSP.NS", "BPCL.NS", "TATACONSUM.NS", "UPL.NS", "VEDL.NS"
]
tickers = st.sidebar.multiselect("Select NSE Stocks:", options = nse_tickers, default = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS"])

weights = []

if tickers:
    st.sidebar.markdown("Assign Portfolio Weights")
    for t in tickers:
        w = st.sidebar.slider(f"Weight for {t}", min_value=0.0, max_value=1.0, value=round(1/len(tickers), 2), step=0.01)
        weights.append(w)
    total = sum(weights)
    if total != 1 and total != 0:
        weights = [w / total for w in weights]

start_date = st.sidebar.date_input(
    "Select Start Date",
    value=pd.to_datetime("2016-01-01"),
    max_value=pd.Timestamp.today()
)
end_date = pd.Timestamp.today()
generate_btn = st.sidebar.button("Generate Analysis")

## Main Logic
if generate_btn:
    if not tickers:
        st.error("Please select at least one stock.")
        st.stop()
    if len(tickers) != len(weights):
        st.error("Tickers and weights mismatch!")
        st.stop()

with st.spinner("Fetching data and computing analytics..."):
    price_data = yf.download(tickers, start=start_date, end=end_date)["Close"]
    returns = price_data.pct_change().dropna()

    portfolio_returns = (returns*weights).sum(axis=1)
    qs.extend_pandas()

    #Display Metrics
    st.subheader("KEY METRICS")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sharpe Ratio", f"{qs.stats.sharpe(portfolio_returns):.2f}")
    col2.metric("Max Drawdown", f"{qs.stats.max_drawdown(portfolio_returns)*100:.2f}%")
    col3.metric("CAGR", f"{qs.stats.cagr(portfolio_returns)*100:.2f}%")
    col4.metric("Volatility", f"{qs.stats.volatility(portfolio_returns)*100:.2f}%")

st.subheader("Portfolio Weights")
fig_pie = px.pie(
    names=tickers,
    values=weights,
    color_discrete_sequence=px.colors.diverging.RdYlGn,
    title="Portfolio Allocation"
)
st.plotly_chart(fig_pie, use_container_width=True)


## Monthly Returns
st.subheader("Monthly Returns Heatmap")
st.dataframe(portfolio_returns.monthly_returns().style.format("{:.2%}"))

## Cumulative Returns Plot
st.subheader("Cumulative Returns")
cumulative = (1 + portfolio_returns).cumprod()
cumulative.name = "Cumulative Return"
fig = px.line(cumulative, color_discrete_sequence=px.colors.diverging.RdYlGn)
st.plotly_chart(fig)

## End-of-Year Returns Chart
st.subheader("End-of-Year (EOY) Returns")
eoy_returns = portfolio_returns.resample("YE").apply(lambda x: (x + 1).prod() - 1)
eoy_returns.name = "Annual Return"
fig = px.bar(eoy_returns, color_discrete_sequence=px.colors.diverging.RdYlGn)
st.plotly_chart(fig)

## Generate HTML Report
with tempfile.TemporaryDirectory() as tmpdir:
    report_path = os.path.join(tmpdir, "portfolio_report.html")
    qs.reports.html(portfolio_returns, output=report_path, title="Portfolio Performance Report")
    with open (report_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        html_content = html_content.replace(
    '#left{width:620px;margin-right:18px;margin-top:-1.2rem;float:left}#right{width:320px;float:right}',
    '#left{width:62%;margin-right:2%;margin-top:-1.2rem;float:left}#right{width:34%;float:right}.container{max-width:100%;padding:0 20px}')
    st.download_button(
        label="Download Full QuantStats Report",
        data=html_content,
        file_name="portfolio_report.html",
        mime="text/html"
    )
st.success("Analysis complete! Explore your portfolio metrics above.")

