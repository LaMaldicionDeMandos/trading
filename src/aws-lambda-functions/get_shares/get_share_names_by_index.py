import logging
import s3_service

logger = logging.getLogger('get_shares_names_by_index')
logger.setLevel(logging.INFO)


def get_share_names(event, context):
    index = event['index']
    try:
        return s3_service.get_share_names_by_index(index)
    except Exception as e:
        raise UserWarning("No se ha encontrado el indice %s." % index)
