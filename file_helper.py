"""Load tcx/gpx/kml data from file, create Workout() from it, export Workout() to various formats."""

import xml.etree.ElementTree as etree
from datetime import datetime
import workout

def convert_time_to_epoch(mytime):
    p = '%Y-%m-%dT%H:%M:%S.%fZ'
    epoch = datetime(1970, 1, 1)
    return int((datetime.strptime(mytime, p) - epoch).total_seconds())

class FileHelper():
    """Helper class to load (import) and save (export) workouts"""
    def __init__(self):
        pass

    def load(self, src_string, user_id):
        """Load workout from tcx/gpx file to Workout() object format."""
        # Some logic to define format based on contents will be implemented later
        file_format = "tcx"
        # Only tcx is implemented in the prototype
        if file_format == "tcx":
            # TCX XML namespace
            NS = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
            # Load tcx
            try:
                root = etree.fromstring(src_string)
            except:
                print("Cannot load XML")
                return None

            # Only the first of activities is processed in the prototype
            activities = root.find("{}Activities".format(NS))
            activity = activities.find('{}Activity'.format(NS))
            id = activity.find('{}Id'.format(NS))
            print("Id.text is: {}".format(id.text))
            timestamp = convert_time_to_epoch(id.text)
            print("Timestamp is: {}".format(timestamp))
            laps = activity.findall('{}Lap'.format(NS))

            # Get temporarily timestamp
            # timestamp = int(datetime.now().timestamp())
            # print("Timestamp is: {}".format(timestamp))

            my_workout = workout.Workout(user_id=user_id, timestamp=timestamp, sport="Biking")

            for i, lap in enumerate(laps):
                # Only the first track is processed in the prototype
                track = lap.find('{}Track'.format(NS))
                trackpoints = track.findall('{}Trackpoint'.format(NS))

                # No stats are processed at this stage in the prototype
                my_lap = workout.Lap({}, i)

                for tp in trackpoints:
                    # Possible values keys are:
                    # time - epoch format
                    # latitude
                    # longitude
                    # altitude
                    # distance
                    # heart_rate
                    # cadence
                    # power - to implement later

                    params = {}
                    time = tp.find('{}Time'.format(NS))

                    # Read and process timestamp
                    try:
                        # Need to add accurate processing of milliseconds
                        my_time = datetime.strptime(time.text, "%Y-%m-%dT%H:%M:%S.000Z")
                        epoch_time = my_time.timestamp()
                        params["time"] = epoch_time
                    except:
                        pass

                    # Read and process geo coordinates
                    try:
                        position = tp.find('{}Position'.format(NS))
                    except:
                        position = None

                    if position is not None:
                        latitude = position.find('{}LatitudeDegrees'.format(NS))
                        try:
                            params["latitude"] = float(latitude.text)
                        except:
                            pass

                        longitude = position.find('{}LongitudeDegrees'.format(NS))
                        try:
                            params["longitude"] = float(longitude.text)
                        except:
                            pass

                    # Altitude
                    altitude = tp.find('{}AltitudeMeters'.format(NS))
                    try:
                        params["altitude"] = float(altitude.text)
                    except:
                        pass

                    # Distance
                    distance = tp.find('{}DistanceMeters'.format(NS))
                    try:
                        params["distance"] = float(distance.text)
                    except:
                        pass

                    # Heart rate
                    hr = tp.find('{}HeartRateBpm'.format(NS))
                    hr_value = hr.find('{}Value'.format(NS))
                    try:
                        params["heart_rate"] = int(hr_value.text)
                    except:
                        pass

                    # Cadence
                    cadence = tp.find('{}Cadence'.format(NS))
                    try:
                        params["cadence"] = int(cadence.text)
                    except:
                        pass

                    # Add trackpoint to a lap
                    my_trackpoint = workout.TrackPoint(params)
                    my_lap.add_trackpoint(my_trackpoint)

                # Add lap to workout
                my_workout.add_lap(my_lap)
                return my_workout

        else:
            print("Only .tcx is supported at the moment")
            return None

    def save(self, filename, file_format):
        """Export Workout() to gpx/tcx/kml/kmz."""
        pass
