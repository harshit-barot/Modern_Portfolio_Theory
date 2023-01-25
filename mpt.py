# -*- coding: utf-8 -*-
"""Modern_Portfolio_Theory_Visualization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BVhKKnWJmUI_Heo6Tot1DJ1AkzhppMtj
"""

# !pip install yfinance
# !pip install get_all_tickers

import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from get_all_tickers import get_tickers as gt
import random

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'wikitable sortable'})
tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text.strip()
    tickers.append(ticker)
print(tickers)

# Prompt user to enter number of stocks to choose
n = int(input("Enter number of stocks to choose randomly: "))

# Verify user input
if n <= 0:
    print("Invalid input. Number of stocks must be greater than 0.")
    exit()
# Get a list of all tickers
tickers_list = tickers

# Choose n stocks randomly from the list
random_stocks = random.sample(tickers_list, n)

# Print the chosen stocks
print("Randomly chosen stocks:")
for stock in random_stocks:
    print(stock)

# Define the stocks to analyze
stocks = random_stocks

# Get stock data
data = yf.download(stocks, start='2015-01-01', end='2020-12-31')

data

data.Close.plot(figsize=(15,10))

# Calculate daily returns
returns = data['Close'].pct_change()
returns

# Calculate mean and covariance of daily returns
mean_returns = returns.mean()
cov_matrix = returns.cov()

print(mean_returns)

print(cov_matrix)

# Set number of simulations and risk-free rate
num_portfolios = 25000
risk_free_rate = 0.0178

# Create an array to hold results
results = np.zeros((3, num_portfolios))

for i in range(num_portfolios):
    # Select random weights for portfolio holdings
    weights = np.random.random(len(stocks))
    # Rebalance weights to sum to 1
    weights /= np.sum(weights)

    # Calculate portfolio return and volatility
    portfolio_return = np.sum(mean_returns * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)

    # Store results in results array
    results[0, i] = portfolio_return
    results[1, i] = portfolio_volatility
    # Store Sharpe Ratio (return / volatility) - risk free rate is subtracted
    results[2, i] = (results[0, i] - risk_free_rate) / results[1, i]

# Convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T, columns=['ret', 'stdev', 'sharpe'])

results_frame

import seaborn as sns
import matplotlib.pyplot as plt

# Set figure size
plt.figure(figsize=(15,10))

# Plot efficient frontier
sns.scatterplot(x='stdev', y='ret', hue='sharpe', data=results_frame)
# Add labels and title
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.title('Efficient Frontier')

# Show plot
plt.show()