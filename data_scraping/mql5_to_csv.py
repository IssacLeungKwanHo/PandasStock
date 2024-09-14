from datetime import datetime
import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# import the 'pandas' module for displaying data obtained in the tabular form
import pandas as pd

pd.set_option('display.max_columns', 500)  # number of columns to be displayed
pd.set_option('display.width', 1500)  # max table width to display
# import pytz module for working with time zone
import pytz

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2024, 1, 10, tzinfo=timezone)
symbol = "AAPL.US"
# get bars from EURUSD M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, utc_from, utc_to)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# display each element of obtained data in a new line
print("Display obtained data 'as is'")
counter = 0
for rate in rates:
    counter += 1
    if counter <= 10:
        print(rate)

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the 'datetime' format
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
#drop the unnecessary columns
rates_frame.drop(['real_volume', 'spread'], axis=1, inplace=True)
# rename columns
rates_frame.rename(columns={'time': 'date', 'tick_volume': 'volume'}, inplace=True)

# display data
print("\nDisplay dataframe with data")
print(rates_frame.head(10))
# save the obtained data as a CSV file
rates_frame.to_csv(f'../data/{symbol}_D1.csv', index=False)

# pip freeze > requirements.txt
# pip install -r requirements.txt