import matplotlib.pyplot as plt
import pandas as pd

from alpha_vantage.timeseries import TimeSeries


def get_stock_data(ts, symbol, start_date, end_date):
    """
    Fetches daily stock prices for a given symbol and returns cumulative
    percentage gains for the selected date range.
    Args:
        ts (TimeSeries): Alpha Vantage TimeSeries client.
        symbol (str): Stock ticker symbol.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
    Returns:
        pandas.Series: Cumulative percentage gains indexed by date.
    """
    try:
        data, _ = ts.get_daily_adjusted(symbol = symbol, outputsize = 'full')
        column = '5. adjusted close'
        print(f"✅ Using adjusted data for {symbol}")
    except ValueError:
        data, _ = ts.get_daily(symbol = symbol, outputsize = 'compact')
        column = '4. close'
        print(f"⚠️ Premium endpoint not available for {symbol}. Using basic daily data.")

    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data = (data[start_date:end_date][column]
            .pct_change()
            .fillna(0)
            .add(1)
            .cumprod()
            .sub(1)
            .mul(100))

    return data


def fetch_and_plot_stocks(api_key):
    """
    Retrieves YTD gain data for NVDA and AMD and generates a comparison plot.
    Args:
        api_key (str): Alpha Vantage API key.
    Returns:
        None: Saves and displays the plot.
    """
    ts = TimeSeries(key = api_key, output_format = 'pandas')

    nvda_data = get_stock_data(ts, 'NVDA', '2025-01-01', '2025-10-29')
    amd_data = get_stock_data(ts, 'AMD', '2025-01-01', '2025-10-29')

    # Plotting the results
    plt.figure(figsize=(10, 5))
    plt.plot(nvda_data.index, nvda_data, label = 'NVDA YTD Gain', color = 'blue')
    plt.plot(amd_data.index, amd_data, label = 'AMD YTD Gain', color = 'red')
    plt.title('YTD Stock Gains of NVDA and AMD from Alpha Vantage')
    plt.xlabel('Date')
    plt.ylabel('YTD Gain (%)')
    plt.legend()
    plt.grid(True)

    plt.savefig('ytd_stock_gains.png')
    plt.show()


# Use your Alpha Vantage API Key here
api_key = "YOUR_API_KEY"  # Replace "YOUR_API_KEY" with your actual API key
fetch_and_plot_stocks(api_key)

