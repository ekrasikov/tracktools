from decimal import *
import boto3
import json
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
                for i in obj:
                    i = convert_to_decimals(i)
                return obj
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
            my_item = {
                'user_id': workout_to_save.user_id,
                'timestamp': workout_to_save.timestamp,
                'sport': workout_to_save.sport,
                'stats': json.dumps(workout_to_save.stats),
                'laps': workout.LapSchema().dump(workout_to_save.laps, many=True)
            }
            response = self.table.put_item(Item=convert_to_decimals(my_item))
            return response
        except:
            print("Cannot save workout to DynamoDB")
            return None

    def load_workout(self, id):
        '''Load workout from storage_endpoint, return workout'''

        def convert_from_decimals(obj):
            '''convert all values from decimals to int and float to use boto3'''
            if isinstance(obj, list):
                for i in xrange(len(obj)):
                    obj[i] = convert_from_decimals(obj[i])
                return obj
            elif isinstance(obj, dict):
                for k in obj:
                    obj[k] = convert_from_decimals(obj[k])
                return obj
            elif isinstance(obj, decimal.Decimal):
                if obj % 1 == 0:
                    return int(obj)
                else:
                    return float(obj)
            else:
                return obj

        pass
