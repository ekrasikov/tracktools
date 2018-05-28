import file_helper
import storage_helper
import workout

INPUT_FILENAME = "data_samples/activity2.tcx"
OUTPUT_FILENAME = "outputs/activity2.json"

if __name__ == "__main__":
    my_file_helper = file_helper.FileHelper()

    with open(INPUT_FILENAME, "r") as f:
        s = f.read()
        my_workout = my_file_helper.load(s)

    print(my_workout)

    # result = workout.LapSchema().dump(my_workout.laps, many=True)
    #
    # with open(OUTPUT_FILENAME, "w") as f:
    #     f.write(str(result))
    #
    # my_storage_helper = storage_helper.StorageHelper('eu-central-1', "https://dynamodb.eu-central-1.amazonaws.com", "WorkoutsTest")
    # result = my_storage_helper.save_workout(my_workout)
    # print(result)
    #
    # result = my_storage_helper.load_workout_json(user_id=1, timestamp=file_helper.TS)
    #
    # w1_json = result
    # print(w1_json)
    # schema = workout.WorkoutSchema()
    # w1_obj = schema.load(w1_json)
    # print(type(w1_obj))
    # print(w1_obj)
