'''Classes definitions for workouts'''
#import datetime

class Workout():
    '''Workout session contains laps'''
    def __init__(self, user_id, date_time, sport = None, stats = None, data = None):
        # Id of owning user
        self.user_id = 1
        # Together with user_id used as workout id in API and database. Need to implement using datetime
        # Should be read from tcx. If not present, than timestamp of the first datapoint.
        # If that's not present, current time.
        self.date_time = date_time
        self.sport = "Unknown" if sport is None else sport
        # Dictionary (distance, avg HR, speed, etc)
        self.stats = [] if stats is None else stats
        self.data = [] if data is None else data

    def __str__(self):
        s = "Workout\n"
        s += "user_ID:   {} \n".format(self.user_id)
        s += "date_time: {} \n".format(str(self.date_time)
        s += "sport:     {} \n".format(self.sport)
        s += str(data)
        return s

    def add_lap(self, lap):
        """Add new lap to the workout"""
        self.laps.append(lap)

    def set_id(self, id):
        '''Set new id (used after workout has been saved to persistent storage with storage_helper)'''
        self.id = id


class Lap():
    '''Lap contains some data (averages and maximums) and a list of trackpoints'''
    def __init__(self, stats, id):
        # Id must be unique only within a workout
        self.id = id
        # Dictionary (distance, avg HR, speed, etc)
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
