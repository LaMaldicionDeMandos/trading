import json
import datetime
import invertir_online_connection
import logging
import s3_service

logger = logging.getLogger('get_historical_share_handler')
logger.setLevel(logging.INFO)


def get_historical_share_handler(event, context):
    index = event['index']
    share = event['stock_share']
    fromDate = event.get('from', '2008-01-01') or '2008-01-01'
    toDate = event.get('to', datetime.date.today().isoformat()) or datetime.date.today().isoformat()
    access_token = invertir_online_connection.connect()

    if (access_token is None):
        return {'statusCode': 500}
    else:
        logger.info("Access token %s" % access_token)
        result = invertir_online_connection.get_historical_share(access_token, index, share, fromDate, toDate)
        return s3_service.put_share(index, share, json.dumps(result))
