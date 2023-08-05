from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import toml
import csv
import finnhub
import os
import time


#import api and secret key from config file
config = toml.load('config/config.toml')
api_key = config['alpaca']['api_key']
secret_key = config['alpaca']['api_secret']
key_api = config['finnhub']['api_key']


companies = {}

'''

#import ticker csv file
with open('smallcap_strong.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line_number, row in enumerate(readCSV):
        if line_number != 0:
            companies[row[0]] = row[1]
'''

#initialize client
#client = StockHistoricalDataClient(api_key, secret_key)

year = 2023
'''
for ticker, company in companies.items():
    #go through tickers of companies
    symbol = ticker

    parameters = StockBarsRequest(
        symbol_or_symbols = symbol,
        timeframe = TimeFrame.Month,
        start = datetime(year, 12, 31),
        end = datetime(year + 1, 6, 30)
    )

    try: 
        stock_bars = client.get_stock_bars(parameters)
        #print(stock_bars.df)
    except:
        continue

    #lookup lobbying expenditures for company
    finnhub_client = finnhub.Client(api_key=key_api)
    time.sleep(1)

    try:
        lobbying_data = finnhub_client.stock_lobbying(symbol, f"2022-6-30", f"2023-4-30")
        #for every stock, create a csv file with the stock data
    except:
        pass

    if lobbying_data['data'] != []:
        keys = lobbying_data["data"][0].keys()
        with open(f"lobbying/{symbol}.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(lobbying_data["data"])


    

#iterate through folder, and for each file, if it is empty, delete it
for filename in os.listdir('lobbying'):
    if os.stat(f"lobbying/{filename}").st_size == 0:
        os.remove(f"lobbying/{filename}")

'''

symbol = 'GRBK'

finnhub_client = finnhub.Client(api_key=key_api)
time.sleep(1)

try:
    lobbying_data = finnhub_client.stock_lobbying(symbol, f"2022-6-30", f"2023-4-30")
    #for every stock, create a csv file with the stock data
except:
    pass

if lobbying_data['data'] != []:
    keys = lobbying_data["data"][0].keys()
    with open(f"lobbying/{symbol}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(lobbying_data["data"])