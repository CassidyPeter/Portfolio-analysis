# Portfolio-analysis

During the pandemic I put together an investment portfolio to try and grasp a loose understanding of finance - in particular quantitative trading. Along the way, I came across methods for assessing the performance of stocks, funds, and portfolios - namely Alpha and Beta. 

This script takes the constituent stocks of a portfolio, along with their respective weights, and compares their performance to a benchmark (SPY in this case).
The result is a simple analysis of the portfolios volatility and return.

The Alpha and Beta values are found using the Capital Asset Pricing Model applied to linear regression.

A sample set of stock tickers and weights is included. Alternatively, fresh portfolio data can be entered.


Dependencies:
 - Matplotlib
 - Pandas-datareader
 - scipy
 - seaborn

![Portfolio](https://github.com/CassidyPeter/Portfolio-analysis/blob/master/Portfolio_analysis.png?raw=true)
