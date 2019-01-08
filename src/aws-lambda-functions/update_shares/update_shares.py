import datetime
import json
import logging
import invertir_online_connection
import s3_service

logger = logging.getLogger('update_shares')
logger.setLevel(logging.INFO)


def update_all(event, context):
    fromDate, toDate = dates_from_event(event)
    access_token = invertir_online_connection.connect()
    logger.info("Access Token: %s" % access_token)
    share_names = s3_service.get_share_names()
    for share_file in share_names:
        update_share(share_file, access_token, fromDate, toDate)


def update_share(share_file, access_token, fromDate, toDate):
    share = s3_service.get_share(share_file)
    index, share_name = get_index_and_share_name(share_file)
    news = invertir_online_connection.get_historical_share(access_token, index, share_name, fromDate, toDate)
    logger.info(news + share)
    s3_service.put_share(index, share_name, json.dumps(news + share))

def get_index_and_share_name(name):
    index = name[:name.index('/')]
    share = name[name.index('/') + 1:name.index('.')]
    return (index, share)


def dates_from_event(event):
    delta = datetime.timedelta(days=1)
    today = datetime.date.today()
    tomorrow = today + delta
    fromDate = event.get('from', today.isoformat()) or today.isoformat()
    toDate = event.get('to', tomorrow.isoformat()) or tomorrow.isoformat()
    return fromDate, toDate