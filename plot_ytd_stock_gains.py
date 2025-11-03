import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


# Fetch stock data for NVDA and IBM from the start of 2025 to October 29, 2025
start_date = "2025-01-01"
end_date = "2025-10-29"
nvda_data = yf.download('NVDA', start = start_date, end = end_date)
ibm_data = yf.download('IBM', start = start_date, end = end_date)

# Calculate the YTD gains
nvda_gain = ((nvda_data['Close'] - nvda_data['Close'].iloc[0]) / nvda_data['Close'].iloc[0]) * 100
ibm_gain = ((ibm_data['Close'] - ibm_data['Close'].iloc[0]) / ibm_data['Close'].iloc[0]) * 100

# Create a plot
plt.figure(figsize = (10, 5))
plt.plot(nvda_gain.index, nvda_gain, label = 'NVDA YTD Gain', color = 'blue')
plt.plot(ibm_gain.index, ibm_gain, label = 'IBM YTD Gain', color = 'red')
plt.title('YTD Stock Gains of NVDA and IBM')
plt.xlabel('Date')
plt.ylabel('Percentage Gain (%)')
plt.legend()
plt.grid(True)

# Save the figure to a file
plt.savefig('ytd_stock_gains.png')
plt.show()
