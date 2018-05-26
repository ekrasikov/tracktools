import marshmallow
import file_helper
import workout

INPUT_FILENAME = "data_samples/activity2.tcx"
OUTPUT_FILENAME = "outputs/activity2.json"

if __name__ == "__main__":
    my_helper = file_helper.FileHelper()
    my_workout = my_helper.load(INPUT_FILENAME, "tcx")

    print(my_workout)

    result = workout.WorkoutSchema().dump(my_workout)

    print(result)

    with open(OUTPUT_FILENAME, "w") as f:
        f.write(str(result))

