import sqlite3
from datetime import datetime

# Connect to the database
try:
    conn = sqlite3.connect('data/stock_prices.db')
except FileNotFoundError:
    # If the database file does not exist, create it
    open('data/stock_prices.db', 'w').close()
    conn = sqlite3.connect('data/stock_prices.db')
c = conn.cursor()

# Drop table if exists
c.execute('''DROP TABLE IF EXISTS stock_prices''')

# Create a table for the stock prices
c.execute('''CREATE TABLE IF NOT EXISTS stock_prices
             (ticker text, date datetime, open real, high real, low real, close real, volume real)''')

# Create a dummy data variable
data = [
    {'ticker': 'AAPL', 't': '2022-01-01 10:00:00', 'o': 100.00, 'h': 105.00, 'l': 99.00, 'c': 104.50, 'v': 1000},
    {'ticker': 'AAPL', 't': '2022-01-02 10:00:00', 'o': 104.50, 'h': 108.00, 'l': 103.50, 'c': 107.00, 'v': 1200},
    {'ticker': 'AAPL', 't': '2022-01-03 10:00:00', 'o': 107.00, 'h': 110.00, 'l': 106.50, 'c': 109.50, 'v': 1500},
    {'ticker': 'AAPL', 't': '2022-01-04 10:00:00', 'o': 109.50, 'h': 112.00, 'l': 108.50, 'c': 111.00, 'v': 1700},
    {'ticker': 'AAPL', 't': '2022-01-05 10:00:00', 'o': 111.00, 'h': 113.00, 'l': 110.00, 'c': 112.00, 'v': 2000}
]


if data:
    # Iterate over the data and insert each row into the database
    for row in data:
        ticker=row['ticker']
        date_str = row['t']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # If the date string is not in the correct format, display an error message
            print(f'Error: Invalid date format for {date_str}')
            continue
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
else:
    # If the data is empty, display an error message
    print('Error: No data to insert')

# Close the connection to the database
conn.close()
