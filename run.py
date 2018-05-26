import file_helper
import storage_helper
import workout

INPUT_FILENAME = "data_samples/simple.tcx"
OUTPUT_FILENAME = "outputs/simple.json"

if __name__ == "__main__":
    my_file_helper = file_helper.FileHelper()
    my_workout = my_file_helper.load(INPUT_FILENAME, "tcx")

    result = workout.LapSchema().dump(my_workout.laps, many=True)

    with open(OUTPUT_FILENAME, "w") as f:
        f.write(str(result))

    my_storage_helper = storage_helper.StorageHelper('eu-central-1', "https://dynamodb.eu-central-1.amazonaws.com", "WorkoutsTest")
    result = my_storage_helper.save_workout(my_workout)
    print(result)
