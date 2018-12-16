import boto3
import logging

logger = logging.getLogger('put_share_history_in_s3')
logger.setLevel(logging.INFO)


def put_share():
    logger.info("Ejecutando el put")
    encoded_string = 'saraza'.encode("utf-8")
    file_name = "/hello.txt"
    s3 = boto3.resource("s3")
    s3.Bucket('marceyaida-trading').put_object(Key=file_name, Body=encoded_string)
