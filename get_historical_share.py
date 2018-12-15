import json
from botocore.vendored import requests
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

INVERTIRONLINE_PATH = 'https://api.invertironline.com/'


def get_historical_share_handler(event, context):
    response = requests.post(INVERTIRONLINE_PATH + 'token',
                             headers={
                                 'content-type': 'application/x-www-form-urlencoded',
                                 'username': os.environ[INVERTIRONLINE_USERNAME],
                                 'password': os.environ[INVERTIRONLINE_PASSWORD]
                             },
                             data={
                                 'username': os.environ[INVERTIRONLINE_USERNAME],
                                 'password': os.environ[INVERTIRONLINE_PASSWORD],
                                 'grant_type': 'password'
                             })
    response.raise_for_status()
    if response.status_code == 200:
        body = response.json()
        access_token = body['access_token']

        response = requests.get(
            'https://api.invertironline.com/api/bcba/titulos/cado/cotizacion/seriehistorica/2018-11-01/2018-11-17/sinajustar',
            headers={
                'Accept': 'application/json',
                'Authorization': 'bearer %s' % access_token
            })
        logger.debug({
            'Accept': 'application/json',
            'Authorization': 'bearer %s' % access_token
        })
        response.raise_for_status()
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    return {
        'statusCode': 200,
        'body': {
            'share': event['share'],
            'env': os.environ['saraza']
        }
    }