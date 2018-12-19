import boto3
import json
import logging
import invertir_online_connection

logger = logging.getLogger('update_shares')
logger.setLevel(logging.INFO)

BUCKET = 'marceyaida-trading'

def update_all(event, context):
    access_token = invertir_online_connection.connect()
    logger.info("Access Token: %s" % access_token)
    s3 = boto3.client("s3")
    share_names = get_share_names(s3)
    for share_name in share_names:
        share = get_share(s3, share_name)
        #Usar los datos que vienen, en share_name esta bcba/meli.json habria que separarlo la fecha hay que usar por defecto la ultima pero se puede tomar por parametro
        news = invertir_online_connection.get_historical_share(access_token, "bcba", "meli", "2018-12-18", "2018-12-19")
        logger.info(str(news))
def get_share_names(s3):
    return map( lambda it: it['Key'], s3.list_objects(Bucket = BUCKET)['Contents'])

def get_share(s3, share_name):
    obj = s3.get_object(Bucket = BUCKET, Key = share_name)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    logger.info("%s -> %d" % (share_name, len(data)))
    return data
