import json
from botocore.vendored import requests
import logging
import os

logger = logging.getLogger('invertir_online_connection')
logger.setLevel(logging.INFO)

INVERTIRONLINE_PATH = 'https://api.invertironline.com/'
INVERTIRONLINE_USERNAME = os.environ['INVERTIRONLINE_USERNAME']
INVERTIRONLINE_PASSWORD = os.environ['INVERTIRONLINE_PASSWORD']

INVERTIRONLINE_SHARES_URL = INVERTIRONLINE_PATH + 'api/%s/titulos/%s/cotizacion/seriehistorica/%s/%s/sinajustar'


def connect():
    response = requests.post(INVERTIRONLINE_PATH + 'token', headers={
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
        return body['access_token']
    return None


def get_historical_share(access_token, index, share, fromDate, toDate):
    url = INVERTIRONLINE_SHARES_URL % (index, share, fromDate, toDate)
    logger.info("URL: %s" % url)
    response = requests.get(
    url,
    headers={
        'Accept': 'application/json',
        'Authorization': 'bearer %s' % access_token
    })
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()
    return None

