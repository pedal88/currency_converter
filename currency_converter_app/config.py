import os

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RATES_FILE = os.path.join(DATA_DIR, 'rates.json')
    ARCHIVE_DIR = os.path.join(DATA_DIR, 'archive')
    
    # Static and template directories
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    
    # API Configuration
    CURRENCY_API_URL = os.environ.get('CURRENCY_API_URL')
    CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY') 