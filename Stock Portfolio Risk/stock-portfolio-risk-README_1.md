# Stock Portfolio Risk & Diversification Analysis

Goal
I wanted to figure out which stocks in a sample portfolio actually gave the best return for the risk you'd be taking on, and whether the portfolio was genuinely diversified or just holding a bunch of stocks that all move the same way.

Code
stock_portfolio_data.py

Description
I used the yfinance library in Python to pull about 5 years of daily price history (2020-2026) for a 7-stock portfolio: Apple, Johnson & Johnson, JPMorgan, Microsoft, Tesla, Exxon, and the S&P 500 as a benchmark. That mix covers tech, finance, healthcare, energy, and one higher-risk growth stock. From the price data I calculated daily returns, then annualized return, volatility, Sharpe ratio, and maximum drawdown for each stock, plus a correlation matrix showing how closely each stock's price moves compared to the others. I also had to reshape the price data in Power Query since it started out with each stock as its own column, and I needed one row per date and ticker instead to build a proper line chart.

Skills used
Pulling financial data through an API, calculating risk and return metrics, reshaping data from wide to long format, and building a heatmap using conditional formatting in Power BI.

Tools
Python (pandas, numpy, yfinance), Power BI

What I found
Tesla had both the highest return (62.6% annualized) and the highest Sharpe ratio (0.90), but also by far the most risk, with 65% volatility and a max drawdown of -73.6%. Johnson & Johnson was the opposite story: the most stable stock in the group, with the lowest volatility and mildest drawdown, but also the lowest raw return. Looking at the correlation matrix, Apple and Microsoft move together pretty closely (0.67), while Johnson & Johnson and Tesla barely relate to each other (0.05), which tells me this portfolio is actually diversified rather than just being different tickers making the same bet.

Dashboard includes
- Line chart showing price history for all 7 stocks
- Bar chart ranking stocks by Sharpe ratio
- Table summarizing all the risk metrics side by side
- Correlation matrix with heatmap coloring

What I'd improve with more time
I'd add a rolling volatility chart to show how risk changed over time instead of one static number for the whole period, and maybe group the stocks by sector to make the diversification story even clearer.
