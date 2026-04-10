import requests
import time
from langchain_core.tools import tool
from utils.logger import get_logger

logger = get_logger()
BASE_URL = "https://restcountries.com/v3.1/name"

@tool
def search_country_data(country_name: str) -> str:
    """
    Search for official intelligence on a specific country.
    """
    if not country_name:
        return "Invalid country focus."
        
    country_clean = country_name.strip()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            url = f"{BASE_URL}/{country_clean}"
            logger.info(f"Accessing Intelligence API: {country_clean}")
            
            res = requests.get(url, timeout=10)

            if res.status_code == 200:
                data = res.json()
                if data and isinstance(data, list):
                    return str(data[0])
                
            if res.status_code == 404:
                return f"Intelligence missing for: '{country_clean}'. Check spelling."
                
        except Exception:
            pass
            
        if attempt < max_retries - 1:
            time.sleep(1)
            
    return "Intelligence service timeout."
