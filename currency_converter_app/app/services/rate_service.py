import os
from datetime import datetime
import json
import shutil
from flask import current_app

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

def get_latest_rates():
    """
    Retrieves the latest rates from the current rates.json file.
    Returns the 'rates' dictionary from the JSON data.
    """
    try:
        with open(current_app.config['RATES_FILE'], 'r') as f:
            data = json.load(f)
            return data.get('rates', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_top_rates():
    """
    Retrieves the top rates from the current rates.json file.
    Returns the 'top_rates' dictionary from the JSON data.
    """
    try:
        with open(current_app.config['RATES_FILE'], 'r') as f:
            data = json.load(f)
            return data.get('top_rates', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_historical_rates(date):
    """
    Retrieves historical rates for a specific date.
    """
    archive_file = os.path.join(current_app.config['ARCHIVE_DIR'], f'rates_{date}.json')
    if os.path.exists(archive_file):
        with open(archive_file, 'r') as f:
            return json.load(f)
    return None 