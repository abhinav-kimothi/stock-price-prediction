import requests
import sqlite3
import json
from datetime import datetime, timedelta
import time

# Set the ticker symbols for the top 10 S&P 500 stocks
ticker_symbols = ['AAPL','MSFT','AMZN','TSLA','GOOGL']

# Set the time span and dates
multiplier = '1'
timespan = 'day'
end_date = datetime.now()
start_date = end_date - timedelta(days=1)  # Update the data for the previous day
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Connect to the database
conn = sqlite3.connect('stock_prices.db')
c = conn.cursor()

# Create a table for the stock prices
c.execute('''CREATE TABLE IF NOT EXISTS stock_prices
             (ticker, date datetime, open real, high real, low real, close real, volume real)''')

# Iterate over the ticker symbols
for ticker in ticker_symbols:
    # Delete all rows for the current ticker and date range
    c.execute('''DELETE FROM stock_prices WHERE ticker = ? AND date >= ? AND date < ?''', (ticker, start_date, end_date))

    # Make the API request to get the stock data
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date_str}/{end_date_str}'
    params = {'adjusted': 'true', 'sort': 'asc', 'limit': '10000', 'apiKey': 'IRWbyzyFiHZDiE8pIaAQqqzpu06_3tjH'}

    response = requests.get(url, params=params)

    # Parse the JSON data in the response
    data = json.loads(response.text)

    print(data)


    if data.get('resultsCount'):
    # Iterate over the data and insert each row into the database
        for row in data.get('results'):
            # Convert the Unix timestamp to a datetime object
            date = datetime.fromtimestamp(row['t'] / 1000)
            open_price = row['o']
            high_price = row['h']
            low_price = row['l']
            close_price = row['c']
            volume = row['v']
            c.execute('''INSERT INTO stock_prices
                     (ticker, date, open, high, low, close, volume) VALUES (?,?,?,?,?,?,?)''',
                  (ticker, date, open_price, high_price, low_price, close_price, volume))

# Save the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
