import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Simple Lambda handler function
    """
    logger.info(f"Event: {json.dumps(event)}")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda!",
            "timestamp": datetime.utcnow().isoformat(),
        }),
    }
