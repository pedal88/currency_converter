import os
from datetime import datetime
import json
import shutil
from flask import current_app
import requests

def manage_rates_file(new_rates_data):
    """
    Manages the daily rates file storage with proper naming convention.
    Creates a new rates file for the current day and archives the previous one.
    """
    # Create data directory if it doesn't exist
    if not os.path.exists(current_app.config['DATA_DIR']):
        os.makedirs(current_app.config['DATA_DIR'])
    
    # Current date in YYYY-MM-DD format
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define file paths
    current_file = current_app.config['RATES_FILE']
    new_file = os.path.join(current_app.config['DATA_DIR'], f'rates_{current_date}.json')
    
    # If current rates.json exists, archive it
    if os.path.exists(current_file):
        # Create archive directory if it doesn't exist
        if not os.path.exists(current_app.config['ARCHIVE_DIR']):
            os.makedirs(current_app.config['ARCHIVE_DIR'])
        
        # Move current file to archive with date
        archive_file = os.path.join(current_app.config['ARCHIVE_DIR'], f'rates_{current_date}.json')
        shutil.move(current_file, archive_file)
    
    # Write new rates data to current rates.json
    with open(current_file, 'w') as f:
        json.dump(new_rates_data, f, indent=4)
    
    # Also save a copy with the date
    with open(new_file, 'w') as f:
        json.dump(new_rates_data, f, indent=4)
    
    return current_file, new_file

def fetch_latest_rates():
    """
    Fetches the latest rates from the ExchangeRate-API.
    Returns None if the request fails.
    """
    try:
        # Get API key from environment variable
        api_key = current_app.config['CURRENCY_API_KEY']
        if not api_key:
            raise ValueError("API key not found. Please set CURRENCY_API_KEY in .env file")

        # Make request to the API
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        data = response.json()
        
        # Create our rates dictionary
        rates_data = {
            "base": "USD",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rates": data['conversion_rates'],
            "top_rates": {
                "EUR": data['conversion_rates']['EUR'],
                "GBP": data['conversion_rates']['GBP'],
                "NOK": data['conversion_rates']['NOK'],
                "DKK": data['conversion_rates']['DKK'],
                "SEK": data['conversion_rates']['SEK']
            }
        }
        
        # Save to file for caching
        save_rates_to_file(rates_data)
        return rates_data
        
    except requests.RequestException as e:
        print(f"Error fetching rates: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def save_rates_to_file(rates_data):
    """
    Saves the rates data to a JSON file.
    """
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(current_app.config['RATES_FILE']), exist_ok=True)
        
        with open(current_app.config['RATES_FILE'], 'w') as f:
            json.dump(rates_data, f, indent=4)
    except Exception as e:
        print(f"Error saving rates to file: {e}")

def get_latest_rates():
    """
    Gets the latest rates, first trying to fetch from the API,
    falling back to the cached file if that fails.
    Returns a tuple of (rates, metadata).
    """
    # Try to get fresh rates from API
    rates_data = fetch_latest_rates()
    
    # If API call fails, try to get cached rates from file
    if rates_data is None:
        try:
            with open(current_app.config['RATES_FILE'], 'r') as f:
                rates_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no cached rates exist, return empty dictionary and no metadata
            return {}, {"source": "No data available", "last_updated": None}
    
    metadata = {
        "source": "ExchangeRate-API" if current_app.config['CURRENCY_API_KEY'] else "Local file",
        "last_updated": rates_data.get('last_updated', 'Unknown date')
    }
    
    return rates_data.get('rates', {}), metadata

def get_top_rates():
    """
    Gets the top rates, first trying to fetch from the API,
    falling back to the cached file if that fails.
    """
    # Try to get fresh rates from API
    rates_data = fetch_latest_rates()
    
    # If API call fails, try to get cached rates from file
    if rates_data is None:
        try:
            with open(current_app.config['RATES_FILE'], 'r') as f:
                rates_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no cached rates exist, return empty dictionary
            return {}
    
    return rates_data.get('top_rates', {})

def get_historical_rates(date):
    """
    Retrieves historical rates for a specific date.
    """
    archive_file = os.path.join(current_app.config['ARCHIVE_DIR'], f'rates_{date}.json')
    if os.path.exists(archive_file):
        with open(archive_file, 'r') as f:
            return json.load(f)
    return None 