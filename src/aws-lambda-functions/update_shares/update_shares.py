import datetime
import boto3
import json
import logging
import invertir_online_connection
from put_share_history_in_s3 import put_share

logger = logging.getLogger('update_shares')
logger.setLevel(logging.INFO)

BUCKET = 'marceyaida-trading'


def update_all(event, context):
    delta = datetime.timedelta(days=1)
    yesterday = datetime.date.today() - delta
    fromDate = event.get('from', yesterday.isoformat()) or yesterday.isoformat()
    toDate = event.get('to', datetime.date.today().isoformat()) or datetime.date.today().isoformat()
    access_token = invertir_online_connection.connect()
    logger.info("Access Token: %s" % access_token)
    s3 = boto3.client("s3")
    share_names = get_share_names(s3)
    for share_file in share_names:
        share = get_share(s3, share_file)
        index, share_name = get_index_and_share_name(share_file)
        news = invertir_online_connection.get_historical_share(access_token, index, share_name, fromDate, toDate)
        logger.info(news + share)
        put_share(index, share_name, json.dumps(news + share))


def get_share_names(s3):
    return map(lambda it: it['Key'], s3.list_objects(Bucket=BUCKET)['Contents'])


def get_share(s3, share_name):
    obj = s3.get_object(Bucket=BUCKET, Key=share_name)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    logger.info("%s -> %d" % (share_name, len(data)))
    return data


def get_index_and_share_name(name):
    index = name[:name.index('/')]
    share = name[name.index('/') + 1:name.index('.')]
    return (index, share)
