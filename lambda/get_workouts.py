import logging
import storage_helper
import os

dynamodb_region = os.environ.get('TRACKTOOLS_DYNAMODB_REGION')
dynamodb_url = os.environ.get('TRACKTOOLS_DYNAMODB_URL')
dynamodb_table = os.environ.get('TRACKTOOLS_DYNAMODB_TABLE')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_workouts_handler(event, context):
    '''List workouts for a user
    GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts
    '''
    try:
        logger.info("Connecting to DB")
        my_storage_helper = storage_helper.StorageHelper(dynamodb_region, dynamodb_url, dynamodb_table)
        logger.info("Loading workout from DB")
        my_workout_dict = my_storage_helper.load_workout_json(user_id=1, timestamp=workout_timestamp)
    except:
        logger.error("Cannot load workout from DB.")
        return {
            'statusCode': 500
        }
    else:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': jsonify(my_workout_dict)
        }