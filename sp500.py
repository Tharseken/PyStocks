# Import Statements
import bs4 as bs
import datetime as dt
import os
import pandas as pd
import numpy as np
import pandas_datareader.data as web 
import matplotlib.pyplot as plt 
from matplotlib import style
import pickle
import requests

style.use("ggplot")

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

def compile_data () :
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv("stock_dfs/{}.csv".format(ticker))
        df.set_index("Date", inplace = True)

        df.rename(columns = {'Adj Close': ticker}, inplace = True)
        df.drop (["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else: 
            main_df = main_df.join(df, how="outer")

        if count % 10 == 0:
            print (count)

    
    print (main_df.head())

    main_df.to_csv("sp500_joined_closes.csv")


def visualize_data():
    df = pd.read_csv("sp500_joined_closes.csv")

    # - Plot an individual stock's data
    # df["AAPL"].plot()
    # plt.show()

    # - Create a correlation dataframe using pandas correlation function
    df_corr = df.corr()
    # print(df_corr.head())

    # - Setup a heatmap for the correlation data
    data = df_corr.values
    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap = plt.cm.RdYlGn)
    figure.colorbar = (heatmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)

    plt.xticks(rotation = 90)
    heatmap.set_clim(-1,1)

    plt.tight_layout()
    plt.show()

visualize_data()