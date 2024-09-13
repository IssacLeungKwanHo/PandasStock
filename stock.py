import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL of the Yahoo Finance markets page
url = 'http://finance.yahoo.com/quote/%5EGSPC/history/'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing market data
table = soup.find('table')

# Extract data from the table
data = []
for row in table.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if cols:
        data.append(cols)

# Create a DataFrame and save it as CSV
df = pd.DataFrame(data, columns=['Date', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
df.to_csv('market_data.csv', index=False)

print("Data saved to market_data.csv")

print(df)