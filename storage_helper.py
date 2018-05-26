from decimal import *
import boto3
import workout

class StorageHelper():
    '''Helper Class to save workout in persistent storage'''
    def __init__(self, region_name, endpoint_url, table_name):
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url)
            self.table = self.dynamodb.Table(table_name)
        except:
            print("Cannot connect to DynamoDB")
        pass

    def save_workout(self, workout_to_save):
        '''Save workout to storage_endpoint, return id'''
        def convert_to_decimals(obj):
            '''convert all values to decimals to use boto3'''
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
            my_item = workout.WorkoutSchema().dump(workout_to_save)
            # Save serialized workout to DynamoDB
            response = self.table.put_item(Item=convert_to_decimals(my_item))
            return response
        except:
            print("Cannot save workout to DynamoDB")
            return None

    def load_workout(self, user_id, timestamp):
        '''Load workout from storage_endpoint, return workout'''
        def convert_from_decimals(obj):
            '''convert all values from decimals to int and float to use boto3'''
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

        print("Response is", response)

        return convert_from_decimals(response)["Item"]
