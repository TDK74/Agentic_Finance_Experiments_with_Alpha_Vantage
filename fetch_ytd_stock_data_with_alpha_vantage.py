import matplotlib.pyplot as plt
import sys
import pandas as pd

from alpha_vantage.timeseries import TimeSeries


def fetch_and_plot_stocks(api_key):
    """
    Retrieves YTD gain data for NVDA and AMD and generates a comparison plot.
    Args:
        api_key (str): Alpha Vantage API key.
    Returns:
        None: Saves and displays the plot.
    """
    ts = TimeSeries(key = api_key, output_format = 'pandas')

    # Fetch the data for NVDA and AMD from the start of the year to the date provided
    # nvda_data, _ = ts.get_daily_adjusted(symbol = 'NVDA', outputsize = 'full')
    try:
        nvda_data, _ = ts.get_daily_adjusted(symbol = 'NVDA', outputsize = 'full')
    except ValueError as e:
        print("⚠️ Premium endpoint not available. " \
            "Use fetch_basic_daily_stock_data.py file "
            "or use fetch_ytd_stock_data_with_AV_enhanced.py file.")
        nvda_data = pd.DataFrame()

    # amd_data, _ = ts.get_daily_adjusted(symbol = 'AMD', outputsize = 'full')
    try:
        amd_data, _ = ts.get_daily_adjusted(symbol = 'AMD', outputsize = 'full')
    except ValueError as e:
        print("⚠️ Premium endpoint not available. " \
            "Use fetch_basic_daily_stock_data.py file "
            "or use fetch_ytd_stock_data_with_AV_enhanced.py file.")
        amd_data = pd.DataFrame()

    # Stop running further to avoid errors due to missing data
    if nvda_data.empty or amd_data.empty:
        print("⚠️ No data returned. Check API limits or symbol spelling.")
        sys.exit()

    # Filter data for the period from 2025-01-01 to 2025-10-29
    nvda_data = (nvda_data['2025-01-01' : '2025-10-29']['5. adjusted close']
                 .pct_change()
                 .fillna(0)
                 .add(1)
                 .cumprod()
                 .sub(1)
                 .mul(100))

    amd_data = (amd_data['2025-01-01' : '2025-10-29']['5. adjusted close']
                .pct_change()
                .fillna(0)
                .add(1)
                .cumprod()
                .sub(1)
                .mul(100))

    # Plotting the results
    plt.figure(figsize = (10, 5))
    plt.plot(nvda_data.index, nvda_data, label = 'NVDA YTD Gain', color = 'blue')
    plt.plot(amd_data.index, amd_data, label = 'AMD YTD Gain', color = 'red')
    plt.title('YTD Stock Gains of NVDA and AMD from Alpha Vantage')
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
