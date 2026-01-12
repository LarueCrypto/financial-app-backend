import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration for all API keys and settings"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Blockchain APIs
    ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '')
    ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY', '')
    POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY', '')
    
    # Banking - Plaid
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID', '')
    PLAID_SECRET = os.getenv('PLAID_SECRET', '')
    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
    
    # AI - OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # News - Finnhub
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')

config = Config()
