import logging
import sys

# Configure logging to stdout for production (e.g., Docker/Heroku/Cloud Run logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("CountryAgent")

def get_logger():
    return logger
