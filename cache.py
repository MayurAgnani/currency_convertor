import time
import configparser  # Import configparser module for reading config files

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')


# Simple in-memory cache
cache = {}
CACHE_EXPIRY = int(config['cache']['expiration_in_seconds'])

def get_cached_rate(from_currency: str, to_currency: str):
    key = f"{from_currency}_{to_currency}"
    if key in cache:
        rate, timestamp = cache[key]
        if time.time() - timestamp < CACHE_EXPIRY:
            return rate
    return None

def set_cached_rate(from_currency: str, to_currency: str, rate: str):
    key = f"{from_currency}_{to_currency}"
    cache[key] = (rate, time.time())
