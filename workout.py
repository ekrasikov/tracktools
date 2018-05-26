'''Classes definitions for workouts'''
import marshmallow

class Workout():
    '''Workout session contains laps'''
    def __init__(self, user_id, date_time, sport=None):
        # Not implemented in a prototype
        self.user_id = user_id
        # date_time along with user_id is used as Workout ID in API and DB
        # need to implement via datetime
        self.date_time = date_time # epoch format
        self.sport = "Unknown" if sport is None else sport
        self.stats = {}
        self.laps = []

    def __str__(self):
        s = "Workout\n"
        s += "user_id:    {} \n".format(str(self.user_id))
        s += "sport: {} \n".format(self.sport)
        for lap in self.laps:
            s += str(lap)
        return s

    def add_lap(self, lap):
        """Add new lap to the workout"""
        self.laps.append(lap)


class Lap():
    '''Lap contains some data (averages and maximums) and a list of trackpoints'''
    def __init__(self, stats, lap_id):
        # Id must be unique only within a workout
        self.lap_id = lap_id
        # Dictionary
        self.stats = stats
        self.trackpoints = []

    def __str__(self):
        s = "Lap\n"
        s += "Lap ID:  {} \n".format(str(self.lap_id))
        for tp in self.trackpoints:
            s += str(tp)
        return s

    def add_trackpoint(self, trackpoint):
        """Add new trackpoint to the lap"""
        self.trackpoints.append(trackpoint)


class TrackPoint():
    '''Trackpoint contains data values: coordinates, speed, heart rate, etc.'''
    def __init__(self, values):
        self.values = values
        """
        Possible values keys are:
        time - epoch format
        latitude
        longitude
        altitude
        distance
        heart_rate
        cadence
        power - to implement later
        """

    def __str__(self):
        s = "Trackpoint\n"

        # Format strings for various parameters
        format_padding = {
            'time': "{:>21}",
            'latitude': "{:>17.5f}",
            'longitude': "{:>16.5f}",
            'altitude': "{:>17.1f}",
            'distance': "{:>17.2f}",
            'heart_rate': "{:>15}",
            'cadence': "{:>18}"
        }

        for key, value in self.values.items():
            try:
                format_string = "{}" + ": " + format_padding[key] + "\n"
                s += format_string.format(key.capitalize(), value)
            except:
                pass

        return s

# class LapEncoder(json.JSONEncoder):
#     '''Encode Lap() to JSON'''
#     def default(self, o):
#         trackpoints_json = ""
#         if isinstance(o, Lap):
#             for t in o.trackpoints:
#                 trackpoints_json += json.dumps(t, cls=TrackPointEncoder)
#                 trackpoints_json += ","
#
#             json_string = '{{ "id" : {} ,'\
#                             '"stats" : {} ,'\
#                             '"trackpoints" : [ {} ]'\
#                         '}}'.format(0, o.stats, trackpoints_json[:-1])
#
#             return json_string
#             #return json.dumps(json_string, sort_keys=False, indent=4)
#         else:
#             json.JSONEncoder.default(self, o)
#
#
# class TrackPointEncoder(json.JSONEncoder):
#     '''Encode TrackPoint() to JSON'''
#     def default(self, o):
#         if isinstance(o, TrackPoint):
#             return o.values
#         else:
#             json.JSONEncoder.default(self, o)


# Marshmallow Schemas definition to serialize
class TrackPointSchema(marshmallow.Schema):
    '''Marshmallow schema to serialize TrackPoint() to JSON'''
    values = marshmallow.fields.Dict()


class LapSchema(marshmallow.Schema):
    '''Marshmallow schema to serialize Lap() to JSON'''
    lap_id = marshmallow.fields.Int()
    stats = marshmallow.fields.Dict()
    trackpoints = marshmallow.fields.Nested(TrackPointSchema, many=True)


class WorkoutSchema(marshmallow.Schema):
    '''Marshmallow schema to serialize Lap() to JSON'''
    user_id = marshmallow.fields.Int()
    date_time = marshmallow.fields.Int() # epoch format
    sport = marshmallow.fields.String()
    stats = marshmallow.fields.Dict()
    laps = marshmallow.fields.Nested(LapSchema, many=True)
