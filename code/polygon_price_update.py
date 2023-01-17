#!/Users/Kim/opt/anaconda3/bin/python
''' we run this script as a daily cron that gets the day's data from polygon'''

import requests
import sqlite3
import json
from datetime import datetime, timedelta
import time
import smtplib
from email.message import EmailMessage
import configparser

config=configparser.ConfigParser()
config.read('../configuration/config.ini')

api_key=config['polygon']['api_key']
pswrd=config['gmail']['password']

# Set the ticker symbols for the top 5 S&P 500 stocks
ticker_symbols = ['AAPL','MSFT','AMZN','TSLA','GOOGL']

# Set the time span and dates
multiplier = '1'
timespan = 'day'
end_date = datetime.now() - timedelta(days=2)
start_date = end_date# Update the data for the previous day
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
end_date=end_date.strftime('%Y-%m-%d %H:%M:%S')
start_date=start_date.strftime('%Y-%m-%d %H:%M:%S')
end_date=datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
start_date=datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)

# Connect to the database
conn = sqlite3.connect('../data/stock_prices_polygon.db')
c = conn.cursor()

# Create a table for the stock prices

c.execute('''CREATE TABLE IF NOT EXISTS stock_prices_polygon
             (ticker, date datetime, open real, high real, low real, close real, volume real)''')

print("Executed 4")

all_data="Today's Update : " + str(start_date)+ ":" +str(end_date)+ "\n\n"
# Iterate over the ticker symbols
for ticker in ticker_symbols:
    c.execute('''SELECT * FROM stock_prices_polygon WHERE ticker = ? AND date >= ? AND date <= ?''', (ticker, start_date, end_date))

    rows=c.fetchall()

    # Make the API request to get the stock data
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date_str}/{end_date_str}'
    params = {'adjusted': 'true', 'sort': 'asc', 'limit': '10000', 'apiKey': api_key}

    response = requests.get(url, params=params)

    # Parse the JSON data in the response
    data = json.loads(response.text)

    all_data+=ticker +'\n' + str(data)+'\n'

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
            # Delete all rows for the current ticker and date range
            c.execute('''DELETE FROM stock_prices_polygon WHERE ticker = ? AND date >= ? AND date <= ?''', (ticker, start_date, end_date))
            c.execute('''INSERT INTO stock_prices_polygon
                     (ticker, date, open, high, low, close, volume) VALUES (?,?,?,?,?,?,?)''',
                  (ticker, date, open_price, high_price, low_price, close_price, volume))
    else:
        all_data+="Looks like the market is closed\n\n\n"

#Send an email when the update is complete

msg = EmailMessage()
msg['From'] = 'abhinavkimothi145@gmail.com'
msg['To'] = 'abhinavkimothids@gmail.com'
msg['Subject'] = 'Stock Price Data Update!'
msg.set_content(all_data)

# Connect to the email server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

# Login to the email server (optional)
server.login('abhinavkimothi145@gmail.com', pswrd)

# Send the message
server.send_message(msg)

# Disconnect from the server
server.quit()

# Save the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
