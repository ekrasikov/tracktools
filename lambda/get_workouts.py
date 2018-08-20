import logging
import storage_helper
import os
import json

dynamodb_region = os.environ.get('TRACKTOOLS_DYNAMODB_REGION')
dynamodb_url = os.environ.get('TRACKTOOLS_DYNAMODB_URL')
dynamodb_table = os.environ.get('TRACKTOOLS_DYNAMODB_TABLE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_workouts_handler(event, context):
    '''List workouts for a user
    GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts
    '''
    logger.info("Got dynamoDB parameters from environment variables:")
    logger.info("region: {}, url: {}, table: {}".format(dynamodb_region, dynamodb_url, dynamodb_table))

    try:
        user_id = int(event['pathParameters']['user_id'])
    except:
        logger.error("Malformed user_id in URL")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': 'Malformed user_id in URL - not integer'
        }

    logger.info("user_id got from path parameters is {}, it's type is {}".format(user_id, type(user_id)))

    try:
        logger.info("Connecting to DB")
        my_storage_helper = storage_helper.StorageHelper(dynamodb_region, dynamodb_url, dynamodb_table)
        logger.info("Loading workouts list from DB")
        my_workouts = my_storage_helper.get_workouts_list(user_id=user_id)
    except:
        logger.error("Cannot load workouts list from DB.")
        return {
            'statusCode': 500
        }
    else:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(my_workouts)
        }