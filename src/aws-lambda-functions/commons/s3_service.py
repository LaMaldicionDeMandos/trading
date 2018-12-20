import boto3
import json
import logging

logger = logging.getLogger('s3_service')
logger.setLevel(logging.INFO)

BUCKET = 'marceyaida-trading'


def put_share(index, share, body):
    logger.info("Ejecutando el put index: %s, share: %s --> %s" % (index, share, body))
    file_name = "%s/%s.json" % (index, share)
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET).put_object(Key=file_name, Body=body)
    return body


def get_share_names():
    s3 = boto3.client("s3")
    return map(lambda it: it['Key'], s3.list_objects(Bucket=BUCKET)['Contents'])


def get_share(share_name):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=BUCKET, Key=share_name)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    logger.info("%s -> %d" % (share_name, len(data)))
    return data