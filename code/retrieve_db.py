import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def retrieve(ticker='AAPL'):
    # Connect to the database
    conn = sqlite3.connect('../data/stock_prices_polygon.db')
    c = conn.cursor()

    # Select all rows from the stock_prices table

    print(ticker)
    c.execute(f'''SELECT * FROM stock_prices_polygon WHERE ticker='{ticker}' ''')

    # Get the column names from the cursor
    column_names = [column[0] for column in c.description]

    # Fetch the rows and store them in a list
    rows = c.fetchall()

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=column_names)

    print(df.sort_values('date'))

    # Close the connection to the database
    conn.close()

    return({"data":df[['date','open']].to_dict()})

retrieve(ticker='AAPL')


