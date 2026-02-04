import json
import logging
import urllib.request
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_exchange_rates():
    """
    Fetch current exchange rates from CNB (Czech National Bank)
    Returns EUR/CZK and USD/CZK rates
    """
    try:
        # Use the official CNB daily exchange rates URL
        urls = [
            "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt",
        ]
        
        content = None
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    content = response.read().decode('utf-8')
                logger.info(f"Successfully fetched from: {url}")
                break
            except Exception as e:
                logger.info(f"Failed to fetch from {url}: {str(e)}")
                continue
        
        if not content:
            raise Exception("Failed to fetch exchange rates from CNB")
        
        rates = {}
        lines = content.strip().split('\n')
        
        # Parse the CNB format
        # Header lines contain date info (starting with #)
        # Data lines format: Country|Currency|Amount|Code|Rate
        for line in lines:
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 5:
                try:
                    country = parts[0].strip()
                    currency = parts[1].strip()
                    amount = int(parts[2].strip())
                    code = parts[3].strip()
                    rate = float(parts[4].replace(',', '.').strip())
                    
                    # Calculate rate per 1 unit
                    rate_per_unit = rate / amount
                    
                    if code == 'EUR':
                        rates['EUR/CZK'] = round(rate_per_unit, 4)
                        logger.info(f"Found EUR rate: {rate_per_unit}")
                    elif code == 'USD':
                        rates['USD/CZK'] = round(rate_per_unit, 4)
                        logger.info(f"Found USD rate: {rate_per_unit}")
                except (ValueError, IndexError) as e:
                    logger.debug(f"Error parsing line: {line} - {str(e)}")
                    continue
        
        if not rates:
            raise Exception("No exchange rates found in CNB data")
        
        return rates
    
    except Exception as e:
        logger.error(f"Error fetching exchange rates: {str(e)}")
        raise


def handler(event, context):
    """
    Lambda handler that returns current EUR/CZK and USD/CZK exchange rates
    """
    logger.info(f"Event: {json.dumps(event)}")
    
    try:
        rates = get_exchange_rates()
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Current CNB Exchange Rates",
                "timestamp": datetime.utcnow().isoformat(),
                "rates": rates,
            }),
        }
    
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to fetch exchange rates",
                "details": str(e),
            }),
        }
