import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime as dt
import re


def sample_portfolio():
    # Tickers and weights of assets in portfolio
    tickers = ['AAPL', 'KO', 'OXY', 'PEP', 'BAC', 'ATO', 'BRKB']
    weights = [0.3416, 0.1246, 0.1444, 0.1195, 0.0618, 0.0897, 0.1184]

    return tickers, weights

def enter_portfolio_data():
    tickers = []
    weights = []
    n = int(input("Number of stocks in portfolio: "))
    for i in range(0,n):
        tickers.append(re.sub('[-.]', "", input("Ticker: ").upper()))
        weights.append(round(float(input("Percentage of portfolio: "))/100,4))
    print("Sum of weights: ", sum(weights))

    return tickers, weights

def dates():
    # Start and end dates of asset data
    print("\n******* Historical start date of portfolio asset data *******\n")
    startyear, startmonth, startday = input("Enter start date (yyyy mm dd): ").split()
    start = dt.datetime(int(startyear), int(startmonth), int(startday))
    print("\n******* End date of portfolio asset data *******\n")
    if input("Collect data up to today?(y/n): ").upper() == 'Y':
        end = dt.datetime.now()
    else:
        endyear, endmonth, endday = input("Enter end date (yyyy mm dd): ").split()
        end = dt.datetime(int(endyear), int(endmonth), int(endday))
    print("\n******* Processing *******\n")

    return start, end

def data_fetching_and_processing(tickers, weights, start, end):
    # Price data of tickers from Yahoo! Finance
    price_data = web.get_data_yahoo(tickers, start, end)
    price_data = price_data['Adj Close']

    # Daily returns of assets
    asset_return_data = price_data.pct_change()[1:]

    # Portfolio returns
    portfolio_returns = (asset_return_data * weights).sum(axis=1)

    benchmark_price = web.get_data_yahoo('SPY', start, end)
    benchmark_returns = benchmark_price["Adj Close"].pct_change()[1:]

    return benchmark_returns, portfolio_returns

def alpha_and_beta(benchmark_returns, portfolio_returns):
    # Slope coefficient of reg line is Beta, intercept is Alpha, according to Capital Asset Pricing Model (CAPM)
    (beta, alpha) = np.polyfit(benchmark_returns.values, portfolio_returns.values, 1)[0:2]
    print("The portfolio Alpha is {}, and the Beta is {}.".format(round(alpha, 6), round(beta, 4)))

    if beta > 1:
        print("\nWithin this period, the portfolio was {}% more volatile than the market".format(round((beta % 1)*100), 4))
    else:
        print("\nWithin this period, the portfolio was {}% less volatile than the market".format(round((1-beta)*100), 4))

    if round(alpha,4) == 0:
        print("and the portfolio performed similarly to the market.")
    elif alpha > 0:
        print("and the portfolio outperformed the market by {}%.".format(round(alpha,4)))
    else:
        print("and the portfolio underperformed the market by {}%.".format(round(alpha, 4)))

    return alpha, beta

def plot_regression(benchmark_returns, portfolio_returns, alpha, beta):
    plt.plot(benchmark_returns.values, portfolio_returns.values, 'o')
    plt.plot(benchmark_returns.values, beta*benchmark_returns.values + alpha)
    plt.xlabel("Benchmark returns")
    plt.ylabel("Portfolio returns")
    plt.title("Portfolio returns vs Benchmark returns (daily) from {}".format(start.date()))
    plt.show()

if __name__ == '__main__':
    if input("\nEnter own portfolio data?(tickers & weights)(y/n): ").upper() == 'Y':
        tickers, weights = enter_portfolio_data()
    else:
        tickers, weights = sample_portfolio()
    start, end = dates()
    benchmark_returns, portfolio_returns =  data_fetching_and_processing(tickers, weights, start, end)
    alpha, beta = alpha_and_beta(benchmark_returns, portfolio_returns)
    plot_regression(benchmark_returns, portfolio_returns, alpha, beta)
