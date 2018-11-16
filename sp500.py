# Import Statements
import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web 
import pickle
import requests

# Scrape tickers from Wikipedia
def save_sp500_tickers():

    # Fetch S&P 500 list from Wiki
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxmlc")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []

    # Parse through Wiki table and append to tickers array
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        tickers.append(ticker)
    
    # Write S&P6
    with open ("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
    # Output list of tickers
    print(tickers)
        
    return tickers

# save_sp500_tickers()


def get_data_from_yahoo (reload_sp500 = False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open ("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2018,10,31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end)
            df.to_csv("stock_dfs/{}.csv".format(ticker))
        else :
            print("Already have {}".format(ticker))


get_data_from_yahoo()