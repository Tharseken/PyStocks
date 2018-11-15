import datetime as dt
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use("ggplot")

# - Generate TESLA stock data using Yahoo web service
# start = dt.datetime(2000, 1, 1)
# end = dt.datetime(2017, 12, 31)
# df = web.DataReader("TSLA", "yahoo", start, end)

# - Export dataframe to csv format
# df.to_csv("TESLA.csv")

# - Read TESLA stock data from created CSV file
df = pd.read_csv("TESLA.csv", parse_dates = True, index_col = 0)

df_ohlc = df["Adj Close"].resample("10D").ohlc()
df_volume = df["Volume"].resample("10D").sum()

df_ohlc.reset_index(inplace=True)

df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

# print(df_ohlc.head())

# - Analyze & Plot Stock Data
# print(df.head())

# - Create a moving average column in dataframe
# df["100ma"] = df["Adj Close"].rolling(window = 100, min_periods = 0).mean()

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex = ax1)
ax1.xaxis_date()

# - Create candlestick graph
candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup= "g")

ax2.filzl_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

# - Render the stock data plot
plt.show()
