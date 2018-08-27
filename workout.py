"""Classes definitions for workouts"""
import marshmallow

class Workout():
    """Represents a workout session recorded by a GPS device.

    Workout contains some data (timestamp, sport, averages, etc.) and a list of laps.

    Public attributes:
    - user_id: Id of the workout owner (integer).
    - workout_id: Internal ID, generated after save to DB (integer).
    - timestamp: Creation time in epoch format (integer) - read from source file.
    - sport: Type of sport - Biking, Running, etc. (string)
    - stats: Workout statistics, e.g. average heart rate or speed
        (dictionary; keys and value types may vary).
    - laps: Laps (list of Lap() objects).

    (user_id, timestamp) uniquely identifies workout.
    """
    def __init__(self, user_id, timestamp, sport=None, stats=None, laps=None):
        self.user_id = user_id
        # (timestamp, user_id) is used as Workout ID in API and DB
        # Workout id will be assigned later after save to DB
        self.workout_id = 0
        self.timestamp = timestamp  # epoch format
        self.sport = "Unknown" if sport is None else sport
        self.stats = {} if stats is None else stats
        self.laps = [] if laps is None else laps

    def __str__(self):
        s = "Workout\n"
        s += "user_id:    {} \n".format(str(self.user_id))
        s += "sport: {} \n".format(self.sport)
        for lap in self.laps:
            s += str(lap)
        return s

    def add_lap(self, lap):
        """Add new lap to the workout."""
        self.laps.append(lap)


class Lap():
    """Represents a lap in a workout.

    Lap contains some data (averages and maximums) and a list of trackpoints.

    Public attributes:
    - lap_id: Lap id, must be unique only within a workout
        (integer, typically starts with 0 and increments).
    - stats: Workout statistics, typically averages and maximums
        (dictionary; keys and value types may vary).
    - trackpoints: Trackpoints (list of TrackPoint() objects).
    """
    def __init__(self, stats, lap_id, trackpoints=None):
        self.lap_id = lap_id
        self.stats = stats
        self.trackpoints = [] if trackpoints is None else trackpoints

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
    """Represents single data point recorded by a GPS device.

    Contains metrics (geo coordinates, speed, heart rate, etc.) for a certain time point.

    Public attribute:
    - values: Dictionary of data values. Keys and value types are not specified, any ones
        should be stored correctly. However, only the following ones are processed at the moment:
        - "time": integer. Timestamp in epoch format.
        - "latitude": float
        - "longitude": float
        - "altitude": float
        - "distance": float
        - "heart_rate": integer
        - "cadence": integer
        - "power": integer, will be implemented later

    """
    def __init__(self, values):
        self.values = values

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
            # What if key is not in format_padding? Add exception or check
            #try:
            format_string = "{}" + ": " + format_padding[key] + "\n"
            s += format_string.format(key.capitalize(), value)
            # except:
            #     pass

        return s


# Marshmallow Schemas definitions for serialization
class TrackPointSchema(marshmallow.Schema):
    """Marshmallow schema to serialize TrackPoint() to JSON"""
    values = marshmallow.fields.Dict()

    @marshmallow.post_load
    def make_trackpoint(self, data):
        # Create new TrackPoint() object from JSON data. Actually not used by me
        print("Hey, I'm make_trackpoint")
        return TrackPoint(values=data['values'])


class LapSchema(marshmallow.Schema):
    """Marshmallow schema to serialize Lap() to JSON"""
    lap_id = marshmallow.fields.Int()
    stats = marshmallow.fields.Dict()
    trackpoints = marshmallow.fields.Nested(TrackPointSchema, many=True)

    @marshmallow.post_load
    def make_lap(self, data):
        # Create new Lap() object from JSON data. Actually not used by me
        # return Lap(stats=data['stats'], lap_id=data['lap_id'], trackpoints=data['trackpoints'])
        print("Hey, I'm make_lap")
        return Lap(**data)


class WorkoutSchema(marshmallow.Schema):
    """Marshmallow schema to serialize Lap() to JSON."""
    user_id = marshmallow.fields.Int()
    workout_id = marshmallow.fields.Int()
    timestamp = marshmallow.fields.Int() # epoch format
    sport = marshmallow.fields.String()
    stats = marshmallow.fields.Dict()
    laps = marshmallow.fields.Nested(LapSchema, many=True)

    @marshmallow.post_load
    def make_workout(self, data):
        # Create new Workout() object from JSON data
        print("Hey, I'm make_workout")
        return Workout(**data)
