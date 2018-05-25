import xml.etree.ElementTree as etree
import workout

class FileHelper():
    '''Helper class to load (import) and save (export) workouts'''
    def __init__(self):
        pass

    def load(self, srcfile, file_format):
        """Load workout from tcx/gpx file to Workout() object format"""
        # Only tcx is implemented in the prototype
        if file_format == "tcx":
            # TCX XML namespace
            NS = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
            # Load tcx
            try:
                tree = etree.parse(srcfile)
                root = tree.getroot()
            except:
                print("ERROR - Can't load XML file: {}".format(srcfile))
                return None

            # Only the first of activities is processed in the prototype
            activities = root.find("{}Activities".format(NS))
            activity = activities.find('{}Activity'.format(NS))
            laps = activity.findall('{}Lap'.format(NS))

            my_workout = workout.Workout("Biking")

            for i,lap in enumerate(laps):
                # Only the first track is processed in the prototype
                track = lap.find('{}Track'.format(NS))
                trackpoints = track.findall('{}Trackpoint'.format(NS))

                # No stats are processed at this stage in the prototype
                my_lap = workout.Lap([], i)

                for tp in trackpoints:
                    params = {}
                    time = tp.find('{}Time'.format(NS))

                    # Read and process timestamp
                    try:
                        # Need to add accurate processing of milliseconds
                        my_time = datetime.strptime(time.text, "%Y-%m-%dT%H:%M:%S.000Z")
                        params["time"] = my_time
                    except:
                        params["time"] = None

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
                            params["latitude"] = None

                        longitude = position.find('{}LongitudeDegrees'.format(NS))
                        try:
                            params["longitude"] = float(longitude.text)
                        except:
                            params["longitude"] = None

                    # Altitude
                    altitude = tp.find('{}AltitudeMeters'.format(NS))
                    try:
                        params["altitude"] = float(altitude.text)
                    except:
                        params["altitude"] = None

                    # Distance
                    distance = tp.find('{}DistanceMeters'.format(NS))
                    try:
                        params["distance"] = float(distance.text)
                    except:
                        params["distance"] = None

                    # Heart rate
                    hr = tp.find('{}HeartRateBpm'.format(NS))
                    hr_value = hr.find('{}Value'.format(NS))
                    try:
                        params["heart_rate"] = int(hr_value.text)
                    except:
                        params["heart_rate"] = None

                    # Cadence
                    cadence = tp.find('{}Cadence'.format(NS))
                    try:
                        params["cadence"] = int(cadence.text)
                    except:
                        params["cadence"] = None

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
        pass

