# Import Statements
import bs4 as bs
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


save_sp500_tickers()