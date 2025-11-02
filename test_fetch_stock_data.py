import yfinance as yf

def test_fetch_stock_data(ticker):
    try:
        # Attempt to fetch historical data
        data = yf.download(ticker, start = "2025-01-01", end = "2025-10-29")

        if data.empty:
            print(f"No data fetched for {ticker}.")
        else:
            print(f"Data fetched successfully for {ticker}.")

    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

# Test fetching data for NVDA and META
test_fetch_stock_data("NVDA")
test_fetch_stock_data("META")
