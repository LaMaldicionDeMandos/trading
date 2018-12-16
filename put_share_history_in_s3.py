import boto3
import logging

logger = logging.getLogger('put_share_history_in_s3')
logger.setLevel(logging.INFO)

def put_share(index, share, body):
    logger.info("Ejecutando el put index: %s, share: %s --> %s" % (index, share, body))
    file_name = "%s/%s.json" % (index, share)
    s3 = boto3.resource("s3")
    s3.Bucket('marceyaida-trading').put_object(Key=file_name, Body=body)
    return body