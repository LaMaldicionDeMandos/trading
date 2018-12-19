import boto3
import json
import logging

logger = logging.getLogger('update_shares')
logger.setLevel(logging.INFO)

BUCKET = 'marceyaida-trading'


def update_all(event, context):
    s3 = boto3.client("s3")
    share_names = get_share_names(s3)
    for share_name in share_names:
        get_share(s3, share_name)


def get_share_names(s3):
    return map(lambda it: it['Key'], s3.list_objects(Bucket=BUCKET)['Contents'])


def get_share(s3, share_name):
    obj = s3.get_object(Bucket=BUCKET, Key=share_name)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    # Esta ultima linea usa len para saber la cantidad de registros que tiene
    logger.info("%s -> %d" % (share_name, len(data)))