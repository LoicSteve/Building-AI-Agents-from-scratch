from tool_registry import tool
import urllib.request
import json
import requests
import yfinance as yf
import os





TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
@tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts currency using latest exchange rates.
    
    Parameters:
        - amount: Amount to convert
        - from_currency: Source currency code (e.g., USD)
        - to_currency: Target currency code (e.g., EUR)
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            
        if "rates" not in data:
            return "Error: Could not fetch exchange rates"
            
        rate = data["rates"].get(to_currency.upper())
        if not rate:
            return f"Error: No rate found for {to_currency}"
            
        converted = amount * rate
        return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"
        
    except Exception as e:
        return f"Error converting currency: {str(e)}"


@tool()
def get_weather(city: str = None, **kwargs) -> str:
    """
    Retrieves the current weather for the specified city using the wttr.in service.
    Accepts either 'city' or an alternative keyword 'location'.
    """
    if city is None:
        city = kwargs.get("location")
    if not city:
        return "Error: No city provided."
    try:
        url = f"http://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Error retrieving weather for {city}: {str(e)}"
    


# Tool: Web Search using Tavily API
@tool()
def web_search(query: str) -> str:
    """
    Uses the Tavily API to search for information on the Internet.
    Ensure that TAVILY_API_KEY is set correctly.
    """
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_images": True,
        "include_raw_content": True,
        "max_results": 4,
    }
    try:
        response = requests.post(url=url, json=payload, timeout=10)
        response.raise_for_status()
        response_j = response.json()
        results = response_j.get("results", [])
        if not results:
            return "No results found."
        formatted_results = ""
        for i, result in enumerate(results, 1):
            title = result.get("title", "No Title")
            snippet = result.get("snippet", "No snippet available")
            formatted_results += f"Result {i}: {title}\n{snippet}\n\n"
        return formatted_results.strip()
    except Exception as e:
        return f"Error during web search: {str(e)}"


# Tool: Generalized Stock Price Tool using dynamic ticker lookup
def get_ticker(company: str) -> str:
    """
    Given a company name, queries Yahoo Finance's search API to obtain the ticker symbol.
    Returns the ticker symbol if found; otherwise, returns None.
    """
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company}"
        headers = {"User-Agent": "Mozilla/5.0"}  # required header
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        data = response.json()
        quotes = data.get("quotes", [])
        if quotes:
            return quotes[0].get("symbol")
        else:
            return None
    except Exception as e:
        return None
    
@tool()
def get_stock_price(company: str) -> str:
    """
    Retrieves the latest stock price for any given company by dynamically looking up its ticker symbol
    via Yahoo Finance's search API and then using yfinance to fetch the current price.
    """
    ticker_symbol = get_ticker(company)
    if not ticker_symbol:
        return f"Could not find a ticker symbol for {company}."
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d")
        if data.empty:
            return f"Could not retrieve data for {company}."
        price = data['Close'].iloc[-1]
        return f"The current stock price of {company} ({ticker_symbol}) is ${price:.2f}"
    except Exception as e:
        return f"Error retrieving stock price for {company}: {str(e)}"