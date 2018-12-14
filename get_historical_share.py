import logging
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_historical_share_handler(event, context):
    return {
            'statusCode': 200,
            'body': {
                'share': event['share'],
                'env': os.environ['saraza']
                }
        }
