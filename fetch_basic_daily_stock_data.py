import matplotlib.pyplot as plt
import pandas as pd

from alpha_vantage.timeseries import TimeSeries


def fetch_and_plot_stocks(api_key):
    """
    Fetches daily stock data for for a given ticker анд for the specified period from Alpha Vantage,
    calculates year-to-date (YTD) percentage gains, and plots the results.   
    Args:
        api_key (str): Alpha Vantage API key for authentication.
    Returns:
        None: Saves plot to file and displays it.
    """
    ts = TimeSeries(key = api_key, output_format = 'pandas')

    # Fetch the basic daily data for NVDA and SLYG from the Alpha Vantage service
    nvda_data, nvda_meta = ts.get_daily(symbol = 'NVDA', outputsize = 'compact')
    slyg_data, slyg_meta = ts.get_daily(symbol = 'SLYG', outputsize = 'compact')

    # Ensure the index is a datetime index
    nvda_data.index = pd.to_datetime(nvda_data.index)
    slyg_data.index = pd.to_datetime(slyg_data.index)

    # Filter data for the period from 2025-01-01 to 2025-10-29 safely
    nvda_data = (nvda_data[
                        (nvda_data.index >= "2025-01-01") & (nvda_data.index <= "2025-10-29")
                        ]['4. close']
                        .pct_change()
                        .fillna(0)
                        .add(1)
                        .cumprod()
                        .sub(1)
                        .mul(100))

    slyg_data = (slyg_data[
                        (slyg_data.index >= "2025-01-01") & (slyg_data.index <= "2025-10-29")
                        ]['4. close']
                        .pct_change()
                        .fillna(0)
                        .add(1)
                        .cumprod()
                        .sub(1)
                        .mul(100))

    # Plotting the results
    plt.figure(figsize = (10, 5))
    plt.plot(nvda_data.index, nvda_data, label = 'NVDA YTD Gain', color = 'blue')
    plt.plot(slyg_data.index, slyg_data, label = 'SLYG YTD Gain', color = 'red')
    plt.title('YTD Stock Gains of NVDA and SLYG from Alpha Vantage')
    plt.xlabel('Date')
    plt.ylabel('YTD Gain (%)')
    plt.legend()
    plt.grid(True)

    # Save the figure
    plt.savefig('ytd_stock_gains.png')
    plt.show()


# Use your Alpha Vantage API Key here
api_key = "YOUR_API_KEY"  # Replace "YOUR_API_KEY" with your actual API key
fetch_and_plot_stocks(api_key)
