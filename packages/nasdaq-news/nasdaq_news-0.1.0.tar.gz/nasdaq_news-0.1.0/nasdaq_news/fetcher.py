import os
import json

def get_news(ticker):
    """
    Returns news data for a given NASDAQ-100 stock ticker.
    
    Parameters:
        ticker (str): Stock symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        dict: Parsed news data as a Python dictionary
    """
    ticker = ticker.upper()
    file_path = os.path.join(os.path.dirname(__file__), "data", f"{ticker}.json")

    if not os.path.exists(file_path):
        raise ValueError(f"No news data available for ticker '{ticker}'")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
