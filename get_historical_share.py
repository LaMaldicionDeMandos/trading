import datetime
import json
from botocore.vendored import requests
import logging
import os

logger = logging.getLogger('get_historical_share_handler')
logger.setLevel(logging.INFO)

INVERTIRONLINE_PATH = 'https://api.invertironline.com/'
INVERTIRONLINE_SHARES_URL = INVERTIRONLINE_PATH + 'api/%s/titulos/%s/cotizacion/seriehistorica/%s/%s/sinajustar'
INVERTIRONLINE_USERNAME = os.environ['INVERTIRONLINE_USERNAME']
INVERTIRONLINE_PASSWORD = os.environ['INVERTIRONLINE_PASSWORD']


def get_historical_share_handler(event, context):
    index = event['index']
    share = event['stock_share']
    fromDate = event.get('from', '2008-01-01')
    toDate = event.get('to', datetime.date.today().isoformat())
    url = INVERTIRONLINE_SHARES_URL % (index, share, fromDate, toDate)
    response = requests.post(INVERTIRONLINE_PATH + 'token',
                             headers={
                                 'content-type': 'application/x-www-form-urlencoded',
                                 'username': INVERTIRONLINE_USERNAME,
                                 'password': INVERTIRONLINE_PASSWORD
                             },
                             data={
                                 'username': INVERTIRONLINE_USERNAME,
                                 'password': INVERTIRONLINE_PASSWORD,
                                 'grant_type': 'password'
                             })

    response.raise_for_status()
    if response.status_code == 200:
        body = response.json()
        access_token = body['access_token']
        response = requests.get(
            url,
            headers={
                'Accept': 'application/json',
                'Authorization': 'bearer %s' % access_token
            })
        response.raise_for_status()
        if response.status_code == 200:
            return {
                'statusCode': 201,
                'body': response.json()
            }
        return {'statusCode': 500}

    return {'statusCode': 500}