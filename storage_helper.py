from decimal import *
import boto3
import workout
import sys
from boto3.dynamodb.conditions import Key

class StorageHelper():
    """Helper Class to save workout in persistent storage"""
    def __init__(self, region_name, endpoint_url, table_name):
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url)
            self.table = self.dynamodb.Table(table_name)
        except:
            print("Cannot connect to DynamoDB")
        pass

    def save_workout(self, workout_to_save):
        """Save workout to storage_endpoint, return id."""
        def convert_to_decimals(obj):
            """Convert all values to decimals to use boto3."""
            if isinstance(obj, list):
                return [convert_to_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                for k in obj:
                    obj[k] = convert_to_decimals(obj[k])
                return obj
            elif isinstance(obj, float):
                return Decimal(str(obj))
            elif isinstance(obj, int):
                return Decimal(obj)
            else:
                return obj

        try:
            # Serialize workout
            my_item, errors = workout.WorkoutSchema().dump(workout_to_save)
            # Save serialized workout to DynamoDB
            response = self.table.put_item(Item=convert_to_decimals(my_item))
            return response
        except:
            print("Cannot save workout to DynamoDB", sys.exc_info())
            return None

    def load_workout_json(self, user_id, timestamp):
        """Load workout from storage_endpoint, return it serialized to JSON.

        Can be used for example for APIs to not to deserialize and serialize again"""
        def convert_from_decimals(obj):
            """Convert all values from decimals to int and float to use boto3."""
            if isinstance(obj, list):
                for i in obj:
                    return [convert_from_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                for k in obj:
                    obj[k] = convert_from_decimals(obj[k])
                return obj
            elif isinstance(obj, Decimal):
                if obj % 1 == 0:
                    return int(obj)
                else:
                    return float(obj)
            else:
                return obj

        try:
            response = self.table.get_item(
                Key={
                    'user_id': user_id,
                    'timestamp': timestamp
                }
            )
        except:
            print("Cannot load workout from DynamoDB")
            return None

#        print("Response from DB is", response)
        result = convert_from_decimals(response)["Item"]
#        print("Loaded workout JSON is", result)

        return result

    def load_workout(self, user_id, timestamp):
        """Load workout from storage_endpoint, return Workout() object."""
        my_workout_json = self.load_workout_json(user_id, timestamp)
        schema = workout.WorkoutSchema()
        my_workout, error = schema.load(my_workout_json)
        return my_workout

    def get_workouts_list(self, user_id):
        """Get workouts list fro a user user_id, return list of ids"""
        try:
            response = self.table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
        except:
            print("Cannot query workouts' ids from DynamoDB", sys.exc_info())
            return None

        items = response['Items']

        result = []

        for i in items:
#            print(int(i['timestamp']))
            result.append(int(i['timestamp']))

        return result