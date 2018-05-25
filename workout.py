'''Classes definitions for workouts'''
import json

class Workout():
    '''Workout session contains laps'''
    def __init__(self, user_id, date_time, sport = None):
        # Not implemented in a prototype
        self.user_id = 1
        # date_time along with user_id is used as Workout ID in API and DB
        # need to implement via datetime
        self.date_time = 0
        self.sport = "Unknow" if sport is None else sport
        self.stats = {}
        self.laps = []

    def __str__(self):
        s = "Workout\n"
        s += "ID:    {} \n".format(str(self.id))
        s += "sport: {} \n".format(self.sport)
        for lap in self.laps:
            s += str(lap)
        return s

    def add_lap(self, lap):
        """Add new lap to the workout"""
        self.laps.append(lap)


class Lap():
    '''Lap contains some data (averages and maximums) and a list of trackpoints'''
    def __init__(self, stats, id):
        # Id must be unique only within a workout
        self.id = id
        # Dictionary
        self.stats = stats
        self.trackpoints = []

    def __str__(self):
        s = "Lap\n"
        s += "ID:  {} \n".format(str(self.id))
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
        time
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
                # Convert time to str manually
                if key == "time":
                    value = str(value)
                s += format_string.format(key.capitalize(), value)
            except:
                pass

        return s


class LapEncoder(json.JSONEncoder):
    def default(self, o):
        trackpoints_json = ""
        if isinstance(o, Lap):
            for t in o.trackpoints:
                trackpoints_json += json.dumps(t, cls=TrackPointEncoder)
                trackpoints_json += ","

            json_string = '{{ "id" : {} ,'\
                            '"stats" : {} ,'\
                            '"trackpoints" : [ {} ]'\
                        '}}'.format(0, o.stats, trackpoints_json[:-1])

            return json_string
            #return json.dumps(json_string, sort_keys=False, indent=4)
        else:
            json.JSONEncoder.default(self, o)


class TrackPointEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TrackPoint):
            return o.values
        else:
            json.JSONEncoder.default(self, o)