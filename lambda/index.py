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
        # CNB provides daily exchange rates in a simple text format
        url = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/central_bank_exchange_rate_fixing/daily.txt"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        rates = {}
        lines = content.strip().split('\n')
        
        # Parse the CNB format
        # Header lines contain date info
        # Data lines format: Country|Currency|Amount|Code|Rate
        for line in lines:
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 5:
                country = parts[0].strip()
                currency = parts[1].strip()
                amount = int(parts[2].strip())
                code = parts[3].strip()
                rate = float(parts[4].strip())
                
                # Calculate rate per 1 unit
                rate_per_unit = rate / amount
                
                if code == 'EUR':
                    rates['EUR/CZK'] = round(rate_per_unit, 4)
                elif code == 'USD':
                    rates['USD/CZK'] = round(rate_per_unit, 4)
        
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
