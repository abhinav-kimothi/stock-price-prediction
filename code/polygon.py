import requests
import sqlite3
from datetime import datetime, timedelta
import time
import json
import configparser

#read config.ini for polygon api key

config=configparser.ConfigParser()
config.read('../configuration/config.ini')

api_key=config['polygon']['api_key']


# Set the ticker symbols for the top 5 S&P 500 stocks
ticker_symbols = ['AAPL','MSFT','AMZN','TSLA','GOOGL']

# Set the time span and dates
multiplier = '1'
timespan = 'day'
end_date = datetime.now()
start_date = end_date - timedelta(days=365*2)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Connect to the database
conn = sqlite3.connect('../data/stock_prices_polygon.db')
c = conn.cursor()

# Delete all rows from the stock_prices table
c.execute('DELETE FROM stock_prices_polygon')

# Set the counter for the number of API calls
api_call_count = 0

# Iterate over the ticker symbols
for ticker in ticker_symbols:
    # Set the API endpoint and parameters
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date_str}/{end_date_str}'
    params = {'adjusted': 'true', 'sort': 'asc', 'limit': '10000', 'apiKey': api_key}

    # Send the GET request and store the response
    response = requests.get(url, params=params)

    print(response.text)

    # Check the status code of the response
    if response.status_code != 200:
        print(f'Error getting data for {ticker}: {response.status_code}')
        continue

    # Get the data from the response
    data = json.loads(response.text)

    print(data)

    # Iterate over the data and insert each row into the database
    for row in data.get('results'):
    # Convert the Unix timestamp to a datetime object
        date = datetime.fromtimestamp(row.get('t') / 1000)
        open_price = row.get('o')
        high_price = row.get('h')
        low_price = row.get('l')
        close_price = row.get('c')
        volume = row.get('v')
        c.execute('''INSERT INTO stock_prices_polygon
                 (ticker, date, open, high, low, close, volume) VALUES (?,?,?,?,?,?,?)''',
              (ticker, date, open_price, high_price, low_price, close_price, volume))
    # Increment the counter for the number of API calls
    api_call_count += 1

    # If the counter is greater than or equal to 5, sleep for 60 seconds
    if api_call_count >= 5:
        time.sleep(60)
        api_call_count = 0

# Save the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
