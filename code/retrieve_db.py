import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data/stock_prices.db')
c = conn.cursor()

# Select all rows from the stock_prices table
c.execute('''SELECT * FROM stock_prices''')

# Get the column names from the cursor
column_names = [column[0] for column in c.description]

# Fetch the rows and store them in a list
rows = c.fetchall()

# Create a DataFrame from the rows
df = pd.DataFrame(rows, columns=column_names)

print(df)

# Close the connection to the database
conn.close()
