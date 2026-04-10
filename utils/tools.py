import requests
import time
from langchain_core.tools import tool
from utils.logger import get_logger

logger = get_logger()
BASE_URL = "https://restcountries.com/v3.1/name"

@tool
def search_country_data(country_name: str) -> str:
    """
    Retrieves comprehensive information about a country from the REST Countries API.
    Use this tool to find data such as population, capital, currencies, region, languages, and more.
    
    Args:
        country_name: The name of the country to search for (e.g., 'Germany', 'Japan').
    """
    if not country_name:
        return "Please provide a valid country name."
        
    country_clean = country_name.strip()
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            url = f"{BASE_URL}/{country_clean}"
            logger.info(f"Tool Invoked: Searching for {country_clean} (Attempt {attempt + 1})")
            
            res = requests.get(url, timeout=10)

            if res.status_code == 200:
                data = res.json()
                if data and isinstance(data, list):
                    # We return the first match as a string for the LLM to process
                    return str(data[0])
                
            if res.status_code == 404:
                return f"No data found for country: '{country_clean}'. Please verify the spelling."
                
            logger.warning(f"API returned status {res.status_code} for {country_clean}")
            
        except Exception as e:
            logger.error(f"Tool Error on attempt {attempt + 1}: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
            
    return "The country information service is temporarily unavailable. Please try again later."
