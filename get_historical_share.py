import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_historical_share_handler(event, context):
    return {
            'statusCode': 200,
            'body': event['share']
        }
