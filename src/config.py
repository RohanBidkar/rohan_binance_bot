import os 
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("API Key and Secret must be set in the .env file") 



client = Client(
api_key=API_KEY,
api_secret= API_SECRET,
requests_params={"verify": True, "timeout": 20})

client.FUTURES_URL="https://testnet.binancefuture.com"