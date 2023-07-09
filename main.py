from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import requests
import toml
import csv
import finnhub


#import api and secret key from config file
config = toml.load('config/config.toml')
api_key = config['alpaca']['api_key']
secret_key = config['alpaca']['api_secret']
key_api = config['finnhub']['api_key']


companies = {}

#import ticker csv file
with open('BAD-holdings.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line_number, row in enumerate(readCSV):
        if line_number != 0:
            companies[row[0]] = row[1]

#initialize client
client = StockHistoricalDataClient(api_key, secret_key)


for company, ticker in companies.items():
    #go through tickers of companies
    symbol = ticker

    parameters = StockBarsRequest(
        symbol_or_symbols = symbol,
        timeframe = TimeFrame.Day,
        start = datetime(2022, 12, 31),
        end = datetime(2023, 1, 7)
    )

    try: 
        stock_bars = client.get_stock_bars(parameters)
        #print(stock_bars.df)
    except:
        continue

    #lookup lobbying expenditures for company
    finnhub_client = finnhub.Client(api_key=key_api)

    print(finnhub_client.stock_lobbying(symbol, "2021-01-01", "2022-06-15"))


