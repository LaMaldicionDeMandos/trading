import logging
import s3_service

logger = logging.getLogger('get_shares_names_by_index')
logger.setLevel(logging.INFO)


def get_share_names(event, context):
    index = event['index']
    return s3_service.get_share_names_by_index(index)
