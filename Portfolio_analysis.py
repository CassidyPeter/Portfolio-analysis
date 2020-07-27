import matplotlib.pyplot as plt
import pandas_datareader as web
from scipy import stats
import seaborn as sns
import datetime as dt
import re

def sample_portfolio():
    # Tickers and weights of assets in portfolio
    tickers = ['AAPL', 'KO', 'OXY', 'PEP', 'BAC', 'ATO', 'BRKB']
    wts = [0.3416, 0.1246, 0.1444, 0.1195, 0.0618, 0.0897, 0.1184]

    return tickers, wts

def enter_portfolio_data():
    tickers = []
    wts = []
    n = int(input("Number of stocks in portfolio: "))
    for i in range(0,n):
        tickers.append(re.sub('[-.]', "", input("Ticker: ").upper()))
        wts.append(round(float(input("Percentage of portfolio: "))/100,4))
    print("Sum of weights: ", sum(wts))

    return tickers, wts

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

def data_fetching_and_processing(tickers, wts, start, end):
    # Price data of tickers from Yahoo! Finance
    price_data = web.get_data_yahoo(tickers, start, end)
    price_data = price_data['Adj Close']

    # Daily returns of assets
    ret_data = price_data.pct_change()[1:]

    # Portfolio returns
    port_ret = (ret_data * wts).sum(axis=1)

    benchmark_price = web.get_data_yahoo('SPY', start, end)
    benchmark_ret = benchmark_price["Adj Close"].pct_change()[1:]

    return benchmark_ret, port_ret

def alpha_and_beta(benchmark_ret, port_ret):
    # Slope coefficient of reg line is Beta, intercept is Alpha, according to Capital Asset Pricing Model (CAPM)
    (beta, alpha) = stats.linregress(benchmark_ret.values, port_ret.values)[0:2]
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

def plot_regression(benchmark_ret, port_ret):
    sns.regplot(benchmark_ret.values, port_ret.values)
    plt.xlabel("Benchmark returns")
    plt.ylabel("Portfolio returns")
    plt.title("Portfolio returns vs Benchmark returns")
    plt.show()

if __name__ == '__main__':
    if input("\nEnter own portfolio data?(tickers & weights)(y/n): ").upper() == 'Y':
        tickers, wts = enter_portfolio_data()
    else:
        tickers, wts = sample_portfolio()
    start, end = dates()
    benchmark_ret, port_ret =  data_fetching_and_processing(tickers, wts, start, end)
    alpha_and_beta(benchmark_ret, port_ret)
    plot_regression(benchmark_ret, port_ret)
