import datetime as dt
import matplotlib.pyplot as plt 
from matplotlib import style
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

# - Analyze & Plot Stock Data
# print(df.head())
df.plot()
plt.show()