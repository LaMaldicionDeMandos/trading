import boto3
import json
import logging

logger = logging.getLogger('s3_service')
logger.setLevel(logging.INFO)

BUCKET = 'marceyaida-trading'
S3 = "s3"


def put_share(index, share, body):
    logger.info("Ejecutando el put index: %s, share: %s --> %s" % (index, share, body))
    file_name = "%s/%s.json" % (index, share)
    s3 = boto3.resource(S3)
    s3.Bucket(BUCKET).put_object(Key=file_name, Body=body)
    return body


def get_share_names():
    s3 = boto3.client(S3)
    return map(lambda it: it['Key'], s3.list_objects(Bucket=BUCKET)['Contents'])


def get_share(share_name):
    s3 = boto3.client(S3)
    obj = s3.get_object(Bucket=BUCKET, Key=share_name)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    logger.info("%s -> %d" % (share_name, len(data)))
    return data


def get_indexes():
    s3 = boto3.client(S3)
    return list(
        map(
            lambda it : it['Prefix'][:-1],
            s3.list_objects(Bucket=BUCKET, Delimiter='/')['CommonPrefixes']))

def get_share_names_by_index(index):
    s3 = boto3.client(S3)
    prefix = "%s/" % index
    return list(
        map(
            lambda it : it['Prefix'][len(index)+1:-1],
            s3.list_objects(Bucket=BUCKET, Prefix=prefix, Delimiter='.')['CommonPrefixes']))
