import json
import file_helper
import workout

FILENAME = "data_samples/simple.tcx"

if __name__ == "__main__":
    my_helper = file_helper.FileHelper()
    workout1 = my_helper.load(FILENAME, "tcx")
    #print(workout1)

    print(workout1.laps[0].trackpoints[0])

    print(json.dumps(workout1.laps[0].trackpoints[0], cls=workout.TrackPointEncoder))
