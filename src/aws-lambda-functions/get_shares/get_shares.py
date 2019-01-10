import datetime
import json
import logging
import s3_service

logger = logging.getLogger('get_shares')
logger.setLevel(logging.INFO)


def get_share(event, context):
    index = event['index']
    share_name = event['stock_share']
    share = s3_service.get_share('%s/%s.json' % (index, share_name))
    return share
