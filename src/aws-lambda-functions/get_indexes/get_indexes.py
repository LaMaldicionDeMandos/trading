import logging
import s3_service

logger = logging.getLogger('get_indexes')
logger.setLevel(logging.INFO)


def get_indexes(event, context):
    return s3_service.get_indexes()
