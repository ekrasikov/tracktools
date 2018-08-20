import logging
import storage_helper
import os
import json

dynamodb_region = os.environ.get('TRACKTOOLS_DYNAMODB_REGION')
dynamodb_url = os.environ.get('TRACKTOOLS_DYNAMODB_URL')
dynamodb_table = os.environ.get('TRACKTOOLS_DYNAMODB_TABLE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_workout_handler(event, context):
    '''Get a workout
    GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts/[workout_timestamp]
    '''
    logger.info("Got dynamoDB parameters from environment variables:")
    logger.info("region: {}, url: {}, table: {}".format(dynamodb_region, dynamodb_url, dynamodb_table))

    try:
        user_id = int(event['pathParameters']['user_id'])
        timestamp = int(event['pathParameters']['workout_timestamp'])
    except:
        logger.error("Malformed user_id or workout_id in URL")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message": "Malformed user_id or workout_id in URL - not integer"}'
        }

    logger.info("user_id got from path parameters is {}, it's type is {}".format(user_id, type(user_id)))

    try:
        logger.info("Connecting to DB")
        my_storage_helper = storage_helper.StorageHelper(dynamodb_region, dynamodb_url, dynamodb_table)
        logger.info("Loading workout from DB")
        my_workout_dict = my_storage_helper.load_workout_json(user_id=user_id, timestamp=timestamp)
    except:
        logger.error("Cannot load workout from DB.")
        return {
            'statusCode': 500
        }
    else:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(my_workout_dict)
        }