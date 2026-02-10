# Portfolio Analytics Dashboard

> "In investing, what is comfortable is rarely profitable." — Robert Arnott

---

## Overview

A comprehensive, interactive web-based portfolio analytics dashboard built with Streamlit that empowers investors to analyze and visualize the performance of Indian stock market portfolios. This tool leverages the power of QuantStats for institutional-grade portfolio analytics, making sophisticated financial analysis accessible through an intuitive interface.

---

## Objective

The primary objective of this project was to create a user-friendly platform that enables investors to:

- Construct custom portfolios from NSE-listed stocks
- Analyze portfolio performance using industry-standard metrics
- Visualize portfolio composition and historical returns
- Generate comprehensive performance reports for informed decision-making

This dashboard bridges the gap between complex quantitative finance and practical investment analysis, providing retail investors with tools typically reserved for institutional traders.

---

## What I Built

### Core Features

**Interactive Portfolio Builder**
- Multi-stock selection from 50 top NSE-listed companies
- Dynamic weight allocation with automatic normalization
- Flexible date range selection for historical analysis

**Real-Time Data Integration**
- Live market data fetching via Yahoo Finance API
- Automatic data validation and processing
- Historical price data spanning user-defined periods

**Comprehensive Analytics Suite**
- Key performance metrics dashboard
- Interactive visualizations using Plotly
- Monthly returns heatmap
- Cumulative returns tracking
- Year-over-year performance comparison

**Professional Reporting**
- Downloadable HTML reports powered by QuantStats
- Responsive report design for various screen sizes
- Complete performance tearsheet generation

---

## Technical Implementation

### Architecture

The application follows a streamlined architecture:

```
User Input → Data Fetching → Portfolio Construction → Analytics Computation → Visualization
```

### Data Processing Pipeline

**1. Data Acquisition**
```python
price_data = yf.download(tickers, start=start_date, end=end_date)["Close"]
```
Fetches closing prices for selected stocks over the specified period.

**2. Returns Calculation**
```python
returns = price_data.pct_change().dropna()
```
Computes daily percentage returns, removing initial NaN values.

**3. Portfolio Aggregation**
```python
portfolio_returns = (returns * weights).sum(axis=1)
```
Calculates weighted portfolio returns by multiplying individual stock returns by their allocated weights.

---

## Key Calculations

### Performance Metrics

**Sharpe Ratio**
```python
qs.stats.sharpe(portfolio_returns)
```
Measures risk-adjusted returns. Higher values indicate better returns per unit of risk taken.

**Maximum Drawdown**
```python
qs.stats.max_drawdown(portfolio_returns) * 100
```
Identifies the largest peak-to-trough decline in portfolio value. Critical for understanding downside risk.

**Compound Annual Growth Rate (CAGR)**
```python
qs.stats.cagr(portfolio_returns) * 100
```
Calculates the geometric mean annual return, providing a smoothed measure of portfolio growth.

**Volatility (Annualized)**
```python
qs.stats.volatility(portfolio_returns) * 100
```
Measures the standard deviation of returns, quantifying portfolio risk.

### Derived Analytics

**Cumulative Returns**
```python
cumulative = (1 + portfolio_returns).cumprod()
```
Tracks the growth of $1 invested at the start date through the end date.

**End-of-Year Returns**
```python
eoy_returns = portfolio_returns.resample("YE").apply(lambda x: (x + 1).prod() - 1)
```
Aggregates daily returns into annual performance metrics for year-over-year comparison.

**Monthly Returns Matrix**
```python
portfolio_returns.monthly_returns()
```
Organizes returns into a calendar-style heatmap showing monthly performance patterns.

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend Framework | Streamlit | Interactive web interface |
| Data Source | yfinance | Real-time market data |
| Analytics Engine | QuantStats | Portfolio performance metrics |
| Data Processing | Pandas | Time series manipulation |
| Visualization | Plotly Express | Interactive charts |
| Report Generation | QuantStats HTML | Professional tearsheets |

---

## Installation & Usage

### Prerequisites

```bash
pip install streamlit yfinance quantstats pandas plotly
```

### Running the Dashboard

```bash
streamlit run app.py
```

### Workflow

1. Select stocks from the NSE universe in the sidebar
2. Adjust portfolio weights for each selected stock
3. Choose analysis start date
4. Click "Generate Analysis" to compute metrics
5. Explore interactive visualizations
6. Download comprehensive HTML report

---

## Portfolio Coverage

The dashboard supports 50 major NSE-listed stocks across sectors:

- **Financial Services**: HDFC Bank, ICICI Bank, Kotak Bank, Axis Bank
- **Technology**: TCS, Infosys, HCL Tech, Wipro, Tech Mahindra
- **Energy**: Reliance, ONGC, BPCL, Coal India, NTPC
- **Automotive**: Maruti Suzuki, Tata Motors, Bajaj Auto, Eicher Motors
- **Consumer Goods**: ITC, Hindustan Unilever, Nestle India, Britannia
- **And many more...**

---

## Output Examples

**Metrics Dashboard**: Real-time KPIs displayed in an organized grid
**Portfolio Allocation**: Interactive pie chart with color-coded segments
**Monthly Returns**: Styled dataframe with percentage formatting
**Cumulative Returns**: Line chart tracking portfolio growth trajectory
**Annual Returns**: Bar chart comparing year-over-year performance
**QuantStats Report**: Comprehensive HTML tearsheet with 40+ metrics

---

## Future Enhancements

- Benchmark comparison (Nifty 50, Sensex)
- Risk-parity portfolio optimization
- Monte Carlo simulation for forward projections
- Custom date range selection for reports
- Multi-currency support for global portfolios
- Integration with real-time trading APIs

---

## Conclusion

This portfolio analytics dashboard transforms complex financial analysis into an accessible, visual experience. By combining modern web technologies with robust quantitative libraries, it empowers investors to make data-driven decisions with confidence.
